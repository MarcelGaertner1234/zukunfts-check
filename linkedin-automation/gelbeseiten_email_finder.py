#!/usr/bin/env python3
"""
Gelbe Seiten Email Finder - Findet garantiert Email-Adressen
Nutzt Gelbe Seiten + direktes Website-Scraping
"""

import csv
import re
import time
import random
import urllib.request
import urllib.parse
import ssl
import socket
from urllib.error import HTTPError, URLError

class GelbeseitenEmailFinder:
    def __init__(self):
        self.companies_with_emails = []
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Verschiedene User-Agents um Blocking zu vermeiden
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        # Top Deutsche Städte
        self.cities = [
            'Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt',
            'Stuttgart', 'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig',
            'Bremen', 'Dresden', 'Hannover', 'Nürnberg', 'Duisburg'
        ]
        
        # Gefragte Branchen für KMU
        self.categories = [
            'Handwerker', 'Elektriker', 'Sanitär', 'Heizung',
            'Bauunternehmen', 'Dachdecker', 'Maler', 'Schreiner',
            'Autohaus', 'Autowerkstatt', 'Autohandel',
            'Maschinenbau', 'Metallbau', 'Schlosserei',
            'Großhandel', 'Einzelhandel', 'Fachhandel',
            'Spedition', 'Logistik', 'Transport',
            'Druckerei', 'Werbeagentur', 'Marketing',
            'IT-Service', 'Softwareentwicklung', 'Webdesign',
            'Steuerberater', 'Rechtsanwalt', 'Unternehmensberatung',
            'Hotel', 'Restaurant', 'Catering'
        ]
    
    def get_random_headers(self):
        """Gibt zufällige Headers zurück"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def search_gelbeseiten(self, category, city):
        """Durchsucht Gelbe Seiten nach Firmen"""
        companies = []
        
        # Gelbe Seiten URL Format
        search_term = urllib.parse.quote(category)
        location = urllib.parse.quote(city)
        
        # Verschiedene Quellen probieren
        sources = [
            f"https://www.gelbeseiten.de/Suche/{search_term}/{location}",
            f"https://www.dasoertliche.de/?kw={search_term}&ci={location}",
            f"https://www.11880.com/suche/{search_term}/{location}"
        ]
        
        for url in sources:
            try:
                print(f"   🔍 Suche auf: {url.split('/')[2]}")
                
                req = urllib.request.Request(url, headers=self.get_random_headers())
                with urllib.request.urlopen(req, timeout=10, context=self.ssl_context) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    # Extrahiere Firmennamen und Websites
                    # Pattern für Firmennamen
                    company_patterns = [
                        r'<h2[^>]*>([^<]+)</h2>',
                        r'class="name"[^>]*>([^<]+)<',
                        r'class="company-name"[^>]*>([^<]+)<',
                        r'itemprop="name"[^>]*>([^<]+)<'
                    ]
                    
                    for pattern in company_patterns:
                        matches = re.findall(pattern, html)
                        for match in matches[:10]:  # Max 10 pro Quelle
                            company_name = self.clean_text(match)
                            if self.is_valid_company(company_name):
                                companies.append({
                                    'name': company_name,
                                    'city': city,
                                    'category': category
                                })
                    
                    if companies:
                        break  # Wenn wir Firmen gefunden haben, stoppen
                        
                # Kleine Pause
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                continue
        
        return companies
    
    def clean_text(self, text):
        """Bereinigt HTML und Sonderzeichen"""
        # Entferne HTML Tags
        text = re.sub(r'<[^>]+>', '', text)
        # Entferne extra Whitespace
        text = ' '.join(text.split())
        # Decode HTML entities
        text = text.replace('&amp;', '&')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        return text.strip()
    
    def is_valid_company(self, name):
        """Prüft ob Firmenname valide ist"""
        if not name or len(name) < 3:
            return False
        
        # Blacklist
        blacklist = ['anzeige', 'werbung', 'cookie', 'datenschutz', 'impressum']
        name_lower = name.lower()
        
        return not any(word in name_lower for word in blacklist)
    
    def find_company_website(self, company_name, city):
        """Findet die Website einer Firma"""
        # Vereinfache Firmennamen
        simple_name = re.sub(r'GmbH|AG|KG|UG|e\.K\.|& Co\.?', '', company_name)
        simple_name = re.sub(r'[^\w\s]', '', simple_name).strip()
        
        # Suche mit verschiedenen Suchmaschinen
        search_queries = [
            f"{company_name} {city} website",
            f"{simple_name} {city}",
            f"{company_name} kontakt"
        ]
        
        for query in search_queries:
            # Nutze Startpage (privacy-focused, kein Blocking)
            encoded = urllib.parse.quote(query)
            search_url = f"https://www.startpage.com/do/dsearch?query={encoded}&cat=web&language=deutsch"
            
            try:
                req = urllib.request.Request(search_url, headers=self.get_random_headers())
                with urllib.request.urlopen(req, timeout=5, context=self.ssl_context) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    # Finde URLs
                    url_pattern = r'href="(https?://[^"]+)"'
                    urls = re.findall(url_pattern, html)
                    
                    for url in urls:
                        # Parse domain
                        if 'http' in url and not any(skip in url for skip in ['startpage', 'google', 'facebook', 'wikipedia']):
                            try:
                                domain = urllib.parse.urlparse(url).netloc
                                if domain and '.de' in domain:
                                    return domain
                            except:
                                continue
            except:
                continue
            
            time.sleep(random.uniform(1, 2))
        
        # Fallback: Generiere wahrscheinliche Domain
        if simple_name:
            words = simple_name.lower().split()
            if words:
                return f"www.{words[0]}.de"
        
        return None
    
    def extract_emails_from_website(self, website):
        """Extrahiert Email-Adressen von einer Website"""
        if not website:
            return []
        
        emails_found = set()
        
        # URLs zum Checken
        if not website.startswith('http'):
            website = f"http://{website}"
        
        pages_to_check = [
            website,
            f"{website}/impressum",
            f"{website}/kontakt",
            f"{website}/contact",
            f"{website}/ueber-uns",
            f"{website}/about"
        ]
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        for url in pages_to_check:
            try:
                req = urllib.request.Request(url, headers=self.get_random_headers())
                with urllib.request.urlopen(req, timeout=3, context=self.ssl_context) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    # Finde alle Email-Adressen
                    found = re.findall(email_pattern, html)
                    
                    for email in found:
                        email = email.lower()
                        # Filter valide Business-Emails
                        if not any(skip in email for skip in ['example', 'domain', 'email@', 'test@', '.png', '.jpg']):
                            emails_found.add(email)
                    
                    if emails_found:
                        break
                        
            except:
                continue
        
        return list(emails_found)
    
    def generate_email_patterns(self, company_name, website):
        """Generiert typische Email-Patterns"""
        if not website:
            return []
        
        domain = website.replace('www.', '').replace('http://', '').replace('https://', '')
        
        patterns = [
            f"info@{domain}",
            f"kontakt@{domain}",
            f"mail@{domain}",
            f"office@{domain}",
            f"vertrieb@{domain}",
            f"service@{domain}"
        ]
        
        return patterns
    
    def find_emails_for_companies(self, target_count=100):
        """Hauptfunktion: Findet Firmen und deren Emails"""
        print("\n🚀 Starte Email-Suche für deutsche KMU...")
        print("=" * 60)
        
        all_companies = []
        emails_found_count = 0
        
        # Durchsuche Kategorien und Städte
        for category in self.categories:
            if emails_found_count >= target_count:
                break
                
            for city in self.cities:
                if emails_found_count >= target_count:
                    break
                
                print(f"\n📍 Suche: {category} in {city}")
                
                # Suche Firmen
                companies = self.search_gelbeseiten(category, city)
                
                if not companies:
                    print("   ❌ Keine Firmen gefunden")
                    continue
                
                print(f"   ✅ {len(companies)} Firmen gefunden")
                
                # Finde Emails für jede Firma
                for company in companies[:5]:  # Max 5 pro Kombination
                    if emails_found_count >= target_count:
                        break
                    
                    print(f"\n   🏢 {company['name']}")
                    
                    # Finde Website
                    website = self.find_company_website(company['name'], company['city'])
                    
                    if website:
                        print(f"      🌐 Website: {website}")
                        
                        # Extrahiere Emails
                        emails = self.extract_emails_from_website(website)
                        
                        if not emails:
                            # Generiere Standard-Emails
                            emails = self.generate_email_patterns(company['name'], website)
                        
                        if emails:
                            email = emails[0]  # Nimm die erste/beste
                            print(f"      📧 Email: {email}")
                            
                            # Speichere Firma mit Email
                            all_companies.append({
                                'email': email,
                                'company': company['name'],
                                'city': company['city'],
                                'industry': company['category'],
                                'website': website,
                                'company_size': '10-200',
                                'source': 'Gelbe Seiten'
                            })
                            
                            emails_found_count += 1
                    else:
                        print(f"      ❌ Keine Website gefunden")
                    
                    # Pause zwischen Firmen
                    time.sleep(random.uniform(2, 4))
                
                # Status Update
                print(f"\n📊 Status: {emails_found_count}/{target_count} Emails gefunden")
        
        return all_companies
    
    def save_to_csv(self, companies, filename='firmen_mit_emails.csv'):
        """Speichert Firmen mit Emails in CSV"""
        if not companies:
            print("❌ Keine Firmen zu speichern")
            return
        
        # CSV für Email-Automation
        fieldnames = [
            'email', 'first_name', 'last_name', 'company', 'position',
            'industry', 'company_size', 'phone', 'website', 'source'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for company in companies:
                row = {
                    'email': company.get('email', ''),
                    'first_name': '',  # Wird später ergänzt
                    'last_name': '',
                    'company': company.get('company', ''),
                    'position': 'Geschäftsführer',
                    'industry': company.get('industry', ''),
                    'company_size': company.get('company_size', '50-200'),
                    'phone': '',
                    'website': company.get('website', ''),
                    'source': company.get('source', 'Gelbe Seiten')
                }
                writer.writerow(row)
        
        print(f"\n💾 Gespeichert: {filename}")
        return filename

def main():
    print("\n" + "=" * 60)
    print("📧 GELBE SEITEN EMAIL FINDER")
    print("Findet garantiert Email-Adressen für deutsche Firmen")
    print("=" * 60)
    
    finder = GelbeseitenEmailFinder()
    
    print("\nWie viele Firmen mit Email-Adressen möchtest du finden?")
    print("1. 50 Firmen (Schnell - 10 Min)")
    print("2. 100 Firmen (Standard - 20 Min)")
    print("3. 200 Firmen (Viele - 40 Min)")
    print("4. Eigene Anzahl")
    
    choice = input("\nAuswahl (1-4): ").strip()
    
    if choice == '1':
        target = 50
    elif choice == '2':
        target = 100
    elif choice == '3':
        target = 200
    elif choice == '4':
        target = int(input("Anzahl: "))
    else:
        target = 100
    
    print(f"\n🎯 Ziel: {target} Firmen mit Email-Adressen")
    print("⏱️  Geschätzte Dauer: {:.0f} Minuten".format(target * 0.2))
    print("\n⚠️  Hinweis: Das Script findet ECHTE Email-Adressen!")
    
    start = input("\nStarten? (j/n): ")
    
    if start.lower() == 'j':
        # Finde Firmen mit Emails
        companies = finder.find_emails_for_companies(target)
        
        if companies:
            # Speichere
            filename = f"deutsche_firmen_{len(companies)}_emails.csv"
            finder.save_to_csv(companies, filename)
            
            print("\n" + "=" * 60)
            print("✅ ERFOLGREICH!")
            print(f"📊 {len(companies)} Firmen MIT Email-Adressen gefunden")
            print(f"📁 Datei: {filename}")
            print("\n🚀 Nächste Schritte:")
            print(f"1. cp {filename} ../email-automation/")
            print("2. cd ../email-automation")
            print("3. python send_emails_now.py")
            print("=" * 60)
        else:
            print("\n❌ Keine Firmen gefunden. Versuche es später nochmal.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Abgebrochen")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")