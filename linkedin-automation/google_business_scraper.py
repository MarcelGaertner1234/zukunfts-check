#!/usr/bin/env python3
"""
Google Business Scraper - Findet automatisch 500+ deutsche KMU
Sammelt Firmendaten aus öffentlichen Quellen
"""

import csv
import re
import time
import random
import urllib.request
import urllib.parse
import ssl
import json
from datetime import datetime

class GoogleBusinessScraper:
    def __init__(self):
        self.companies = []
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Deutsche Städte (Top 50)
        self.cities = [
            'Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt',
            'Stuttgart', 'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig',
            'Bremen', 'Dresden', 'Hannover', 'Nürnberg', 'Duisburg',
            'Bochum', 'Wuppertal', 'Bielefeld', 'Bonn', 'Münster',
            'Karlsruhe', 'Mannheim', 'Augsburg', 'Wiesbaden', 'Mönchengladbach',
            'Gelsenkirchen', 'Braunschweig', 'Aachen', 'Kiel', 'Chemnitz',
            'Halle', 'Magdeburg', 'Freiburg', 'Krefeld', 'Lübeck',
            'Mainz', 'Erfurt', 'Oberhausen', 'Rostock', 'Kassel',
            'Hagen', 'Hamm', 'Saarbrücken', 'Mülheim', 'Potsdam',
            'Ludwigshafen', 'Oldenburg', 'Leverkusen', 'Osnabrück', 'Solingen'
        ]
        
        # Branchen für KMU
        self.industries = [
            'Handwerk', 'Bauunternehmen', 'Elektriker', 'Sanitär',
            'Maschinenbau', 'Metallbau', 'Schreinerei', 'Malerbetrieb',
            'Handel', 'Großhandel', 'Einzelhandel', 'Autohaus',
            'Produktion', 'Fertigung', 'Herstellung', 'Fabrik',
            'Logistik', 'Spedition', 'Transport', 'Lagerlogistik',
            'IT-Dienstleister', 'Software', 'Beratung', 'Marketing',
            'Gastronomie', 'Hotel', 'Restaurant', 'Catering',
            'Gesundheit', 'Pflege', 'Medizintechnik', 'Pharma',
            'Immobilien', 'Hausverwaltung', 'Makler', 'Facility',
            'Druckerei', 'Werbeagentur', 'Eventmanagement', 'Messebau'
        ]
        
        # Suchbegriffe für Geschäftsführer
        self.search_terms = [
            'Geschäftsführer',
            'Inhaber',
            'CEO',
            'Vorstand',
            'Gesellschafter',
            'Eigentümer',
            'Betriebsleiter',
            'Prokurist'
        ]
        
        # Firmengröße Keywords
        self.size_keywords = [
            '10 bis 50 Mitarbeiter',
            '50 bis 200 Mitarbeiter',
            '20 bis 100 Mitarbeiter',
            'Mittelstand',
            'KMU',
            'mittelständisch'
        ]
    
    def search_companies(self, query, city="", limit=20):
        """Sucht Firmen basierend auf Query"""
        results = []
        
        # Erstelle Suchanfrage
        if city:
            search_query = f"{query} {city} Deutschland Firma Kontakt"
        else:
            search_query = f"{query} Deutschland Mittelstand"
        
        # URL encode
        encoded_query = urllib.parse.quote_plus(search_query)
        
        # Nutze DuckDuckGo HTML Suche (keine API nötig)
        search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        try:
            req = urllib.request.Request(search_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10, context=self.ssl_context) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Extrahiere Firmeninformationen
                # Pattern für Firmennamen
                company_pattern = r'<a[^>]*class="result__a"[^>]*>([^<]+)</a>'
                companies_found = re.findall(company_pattern, html)
                
                # Pattern für Snippets (enthält oft Kontaktinfo)
                snippet_pattern = r'<a class="result__snippet"[^>]*>([^<]+)</a>'
                snippets = re.findall(snippet_pattern, html)
                
                for i, company_text in enumerate(companies_found[:limit]):
                    # Bereinige Firmennamen
                    company_name = self.clean_company_name(company_text)
                    
                    if company_name and self.is_valid_company(company_name):
                        company_data = {
                            'company': company_name,
                            'city': city,
                            'industry': query,
                            'found_via': 'search',
                            'snippet': snippets[i] if i < len(snippets) else ''
                        }
                        
                        # Versuche Größe zu ermitteln
                        company_data['company_size'] = self.estimate_company_size(company_data['snippet'])
                        
                        results.append(company_data)
                
        except Exception as e:
            print(f"   ⚠️ Fehler bei Suche: {e}")
        
        return results
    
    def clean_company_name(self, text):
        """Bereinigt Firmennamen"""
        # Entferne HTML und unwichtige Zeichen
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[\|\-–—].*', '', text)
        text = text.strip()
        
        # Prüfe ob es ein Firmenname ist
        if len(text) < 3 or len(text) > 100:
            return None
        
        # Muss Firmen-Keywords enthalten
        company_keywords = ['GmbH', 'AG', 'KG', 'UG', 'OHG', 'GbR', 'e.K.', '& Co', 'Group', 'Gruppe']
        
        # Oder typische Firmennamen-Pattern
        if not any(kw in text for kw in company_keywords):
            # Prüfe ob es wie ein Firmenname aussieht
            if not re.match(r'^[A-Z]', text):  # Beginnt mit Großbuchstabe
                return None
        
        return text
    
    def is_valid_company(self, name):
        """Prüft ob es ein valider Firmenname ist"""
        if not name:
            return False
        
        # Blacklist für irrelevante Ergebnisse
        blacklist = [
            'wikipedia', 'facebook', 'linkedin', 'xing',
            'kununu', 'indeed', 'stepstone', 'jobs',
            'impressum', 'datenschutz', 'agb', 'cookie'
        ]
        
        name_lower = name.lower()
        return not any(word in name_lower for word in blacklist)
    
    def estimate_company_size(self, text):
        """Schätzt Firmengröße basierend auf Text"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['1-9 mitarbeiter', 'kleinstunternehmen']):
            return '1-9'
        elif any(kw in text_lower for kw in ['10-49', '10 bis 50', 'kleinunternehmen']):
            return '10-50'
        elif any(kw in text_lower for kw in ['50-199', '50 bis 200', 'mittelstand']):
            return '50-200'
        elif any(kw in text_lower for kw in ['200-499', '200 bis 500']):
            return '200-500'
        else:
            return '10-50'  # Default für KMU
    
    def find_contact_person(self, company_name):
        """Versucht Geschäftsführer zu finden"""
        # Suche nach Geschäftsführer
        search_query = f'"{company_name}" Geschäftsführer OR Inhaber OR CEO'
        encoded = urllib.parse.quote_plus(search_query)
        
        search_url = f"https://html.duckduckgo.com/html/?q={encoded}"
        
        try:
            req = urllib.request.Request(search_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5, context=self.ssl_context) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Suche nach Personennamen
                # Pattern: Vorname Nachname als Geschäftsführer/CEO/Inhaber
                patterns = [
                    r'([A-Z][a-zäöü]+ [A-Z][a-zäöü]+)(?:,?\s*(?:Geschäftsführer|CEO|Inhaber))',
                    r'(?:Geschäftsführer|CEO|Inhaber)(?::|,?\s+)([A-Z][a-zäöü]+ [A-Z][a-zäöü]+)',
                    r'([A-Z][a-zäöü]+ [A-Z][a-zäöü]+)(?:\s+ist\s+(?:Geschäftsführer|CEO|Inhaber))'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, html)
                    if matches:
                        name = matches[0]
                        if isinstance(name, tuple):
                            name = name[0]
                        
                        # Validiere Namen
                        if self.is_valid_person_name(name):
                            parts = name.split()
                            if len(parts) >= 2:
                                return {
                                    'first_name': parts[0],
                                    'last_name': ' '.join(parts[1:]),
                                    'position': 'Geschäftsführer'
                                }
                
        except Exception:
            pass
        
        # Fallback: Generische Werte
        return {
            'first_name': '',
            'last_name': '',
            'position': 'Geschäftsführer'
        }
    
    def is_valid_person_name(self, name):
        """Prüft ob es ein valider Personenname ist"""
        if not name or len(name) < 5 or len(name) > 50:
            return False
        
        # Muss aus 2+ Teilen bestehen
        parts = name.split()
        if len(parts) < 2:
            return False
        
        # Blacklist
        blacklist = ['GmbH', 'AG', 'KG', 'Herr', 'Frau', 'Dr.', 'Prof.']
        return not any(word in name for word in blacklist)
    
    def extract_website(self, company_name):
        """Versucht Website zu finden"""
        # Vereinfache Firmennamen für Domain-Suche
        simple_name = company_name.lower()
        simple_name = re.sub(r'gmbh|ag|kg|ug|ohg|gbr|& co\.?|gruppe|group', '', simple_name)
        simple_name = re.sub(r'[^a-z0-9äöü\s]', '', simple_name)
        simple_name = simple_name.strip()
        
        if simple_name:
            # Häufige Domain-Pattern
            words = simple_name.split()
            if words:
                possible_domains = [
                    f"www.{words[0]}.de",
                    f"www.{words[0]}.com",
                    f"www.{'-'.join(words)}.de",
                    f"www.{''.join(words)}.de"
                ]
                
                # Nimm die erste als wahrscheinlichste
                return possible_domains[0]
        
        return ""
    
    def generate_email(self, first_name, last_name, website):
        """Generiert wahrscheinliche Email-Adresse"""
        if not website:
            return ""
        
        domain = website.replace('www.', '')
        
        if first_name and last_name:
            # Deutsche Umlaute ersetzen
            first = first_name.lower().replace('ä','ae').replace('ö','oe').replace('ü','ue')
            last = last_name.lower().replace('ä','ae').replace('ö','oe').replace('ü','ue')
            
            # Häufigstes Pattern in Deutschland
            return f"{first}.{last}@{domain}"
        else:
            return f"info@{domain}"
    
    def scrape_companies(self, target_count=500):
        """Hauptfunktion: Sammelt target_count Firmen"""
        print(f"\n🚀 Starte Suche nach {target_count} deutschen KMU...")
        print("=" * 60)
        
        companies_found = []
        
        # Mische Städte und Branchen für Vielfalt
        random.shuffle(self.cities)
        random.shuffle(self.industries)
        
        # Suche Kombinationen
        for industry in self.industries:
            if len(companies_found) >= target_count:
                break
            
            for city in self.cities[:10]:  # Top 10 Städte pro Branche
                if len(companies_found) >= target_count:
                    break
                
                print(f"\n🔍 Suche: {industry} in {city}")
                
                # Suche Firmen
                results = self.search_companies(industry, city, limit=5)
                
                for company_data in results:
                    if len(companies_found) >= target_count:
                        break
                    
                    company_name = company_data['company']
                    print(f"   ✓ {company_name}")
                    
                    # Finde Kontaktperson
                    contact = self.find_contact_person(company_name)
                    
                    # Finde Website
                    website = self.extract_website(company_name)
                    
                    # Generiere Email
                    email = self.generate_email(
                        contact['first_name'],
                        contact['last_name'],
                        website
                    )
                    
                    # Erstelle vollständigen Datensatz
                    full_data = {
                        'first_name': contact['first_name'],
                        'last_name': contact['last_name'],
                        'position': contact['position'],
                        'company': company_name,
                        'industry': industry,
                        'company_size': company_data['company_size'],
                        'city': city,
                        'website': website,
                        'email': email,
                        'linkedin_url': '',
                        'phone': '',
                        'source': 'Google'
                    }
                    
                    companies_found.append(full_data)
                    
                    # Status Update
                    if len(companies_found) % 10 == 0:
                        print(f"\n📊 Status: {len(companies_found)}/{target_count} Firmen gefunden")
                
                # Pause zwischen Suchen
                time.sleep(random.uniform(1, 3))
        
        print(f"\n✅ Fertig! {len(companies_found)} Firmen gefunden")
        return companies_found
    
    def save_to_csv(self, companies, filename='german_companies_500.csv'):
        """Speichert Firmen in CSV"""
        if not companies:
            print("❌ Keine Firmen zu speichern")
            return
        
        # CSV Headers
        fieldnames = [
            'email', 'first_name', 'last_name', 'company', 'position',
            'industry', 'company_size', 'city', 'website', 'phone',
            'linkedin_url', 'source'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for company in companies:
                # Ordne Felder für Email-Automation
                row = {
                    'email': company.get('email', ''),
                    'first_name': company.get('first_name', ''),
                    'last_name': company.get('last_name', ''),
                    'company': company.get('company', ''),
                    'position': company.get('position', 'Geschäftsführer'),
                    'industry': company.get('industry', ''),
                    'company_size': company.get('company_size', '50-200'),
                    'city': company.get('city', ''),
                    'website': company.get('website', ''),
                    'phone': company.get('phone', ''),
                    'linkedin_url': company.get('linkedin_url', ''),
                    'source': company.get('source', 'Google')
                }
                writer.writerow(row)
        
        print(f"💾 Gespeichert in: {filename}")
        return filename

def main():
    print("\n" + "=" * 60)
    print("🔍 GOOGLE BUSINESS SCRAPER")
    print("Findet automatisch deutsche KMU für deine Kampagne")
    print("=" * 60)
    
    scraper = GoogleBusinessScraper()
    
    print("\nOptionen:")
    print("1. 500 Firmen sammeln (Empfohlen)")
    print("2. 100 Firmen sammeln (Schnell-Test)")
    print("3. 1000 Firmen sammeln (Dauert länger)")
    print("4. Eigene Anzahl")
    
    choice = input("\nAuswahl (1-4): ").strip()
    
    if choice == '1':
        target = 500
    elif choice == '2':
        target = 100
    elif choice == '3':
        target = 1000
    elif choice == '4':
        target = int(input("Wie viele Firmen? "))
    else:
        target = 500
    
    print(f"\n🎯 Ziel: {target} Firmen")
    print("⏱️ Geschätzte Dauer: {:.0f} Minuten".format(target * 0.2))
    
    start = input("\nStarten? (j/n): ")
    
    if start.lower() == 'j':
        # Sammle Firmen
        companies = scraper.scrape_companies(target)
        
        if companies:
            # Speichere in CSV
            filename = f"german_companies_{len(companies)}.csv"
            scraper.save_to_csv(companies, filename)
            
            print("\n" + "=" * 60)
            print("✅ ERFOLGREICH ABGESCHLOSSEN!")
            print(f"📊 {len(companies)} Firmen gefunden und gespeichert")
            print(f"📁 Datei: {filename}")
            print("\n📧 Nächste Schritte:")
            print(f"1. Kopiere {filename} nach ../email-automation/")
            print("2. cd ../email-automation")
            print("3. python send_emails_now.py")
            print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Abgebrochen")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")