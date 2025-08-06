#!/usr/bin/env python3
"""
Email Finder - Findet automatisch Email-Adressen für LinkedIn-Kontakte
Nutzt Web-Scraping und Pattern-Matching
"""

import csv
import re
import time
import random
import json
from urllib.parse import urlparse, quote_plus
import urllib.request
import urllib.error
import ssl
import socket

class EmailFinder:
    def __init__(self):
        self.found_emails = {}
        self.email_patterns = [
            '{first}.{last}@{domain}',
            '{first}{last}@{domain}',
            '{f}.{last}@{domain}',
            '{first}@{domain}',
            '{last}@{domain}',
            'info@{domain}',
            'kontakt@{domain}',
            'contact@{domain}',
            'office@{domain}',
            'mail@{domain}',
            'hello@{domain}',
            'team@{domain}'
        ]
        
        # SSL Context für HTTPS
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # User-Agent um Blocking zu vermeiden
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def clean_company_name(self, company):
        """Entfernt GmbH, AG, etc. für bessere Suche"""
        cleaners = [
            ' GmbH', ' AG', ' KG', ' OHG', ' GbR', ' UG',
            ' e.V.', ' & Co.', ' Group', ' Gruppe',
            ' gmbh', ' ag', ' kg', ' ohg', ' gbr', ' ug'
        ]
        
        cleaned = company
        for cleaner in cleaners:
            cleaned = cleaned.replace(cleaner, '')
        
        return cleaned.strip()
    
    def search_company_website(self, company_name):
        """Sucht die Website einer Firma via DuckDuckGo (keine API nötig)"""
        print(f"   🔍 Suche Website für: {company_name}")
        
        cleaned_name = self.clean_company_name(company_name)
        
        # Verschiedene Suchanfragen probieren
        search_queries = [
            f"{company_name}",
            f"{cleaned_name}",
            f"{cleaned_name} Deutschland",
            f"{cleaned_name} Impressum"
        ]
        
        for query in search_queries:
            # URL für DuckDuckGo HTML-Suche
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            
            try:
                req = urllib.request.Request(search_url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=5, context=self.ssl_context) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    # Finde URLs in den Suchergebnissen
                    url_pattern = r'href="(https?://[^"]+)"'
                    urls = re.findall(url_pattern, html)
                    
                    # Filtere relevante Business-Domains
                    for url in urls:
                        if any(skip in url for skip in ['duckduckgo', 'google', 'facebook', 'linkedin', 'wikipedia']):
                            continue
                        
                        # Extrahiere Domain
                        parsed = urlparse(url)
                        domain = parsed.netloc.lower()
                        
                        # Prüfe ob es eine deutsche Business-Domain ist
                        if domain and ('.de' in domain or '.com' in domain):
                            # Versuche die Domain zu erreichen
                            if self.verify_domain(domain):
                                print(f"   ✅ Website gefunden: {domain}")
                                return domain
                            
            except Exception as e:
                continue
            
            time.sleep(random.uniform(0.5, 1.5))
        
        return None
    
    def verify_domain(self, domain):
        """Prüft ob eine Domain erreichbar ist"""
        try:
            socket.gethostbyname(domain)
            return True
        except:
            return False
    
    def scrape_website_for_emails(self, domain):
        """Durchsucht Website nach Email-Adressen"""
        emails_found = set()
        
        # URLs zum Prüfen
        pages_to_check = [
            f"https://{domain}",
            f"https://{domain}/impressum",
            f"https://{domain}/imprint",
            f"https://{domain}/kontakt",
            f"https://{domain}/contact",
            f"https://{domain}/about",
            f"https://{domain}/team",
            f"http://{domain}"
        ]
        
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        for url in pages_to_check:
            try:
                req = urllib.request.Request(url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=3, context=self.ssl_context) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    # Finde alle Email-Adressen
                    found = re.findall(email_regex, html)
                    
                    # Filtere relevante Emails
                    for email in found:
                        email = email.lower()
                        # Ignoriere Beispiel-Emails und Images
                        if not any(skip in email for skip in ['example', 'domain', '.png', '.jpg', 'email@']):
                            if domain.replace('www.', '') in email:
                                emails_found.add(email)
                    
                    if emails_found:
                        break
                        
            except Exception:
                continue
        
        return list(emails_found)
    
    def generate_email_patterns(self, first_name, last_name, domain):
        """Generiert mögliche Email-Adressen basierend auf Patterns"""
        if not domain:
            return []
        
        # Entferne www. falls vorhanden
        domain = domain.replace('www.', '')
        
        first = first_name.lower() if first_name else ''
        last = last_name.lower() if last_name else ''
        f = first[0] if first else ''
        
        # Deutsche Umlaute ersetzen
        replacements = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
            'ß': 'ss', 'é': 'e', 'è': 'e'
        }
        
        for old, new in replacements.items():
            first = first.replace(old, new)
            last = last.replace(old, new)
        
        generated = []
        
        for pattern in self.email_patterns:
            try:
                email = pattern.format(
                    first=first,
                    last=last,
                    f=f,
                    domain=domain
                )
                if '@' in email and '.' in email:
                    generated.append(email)
            except:
                continue
        
        return generated
    
    def find_email_for_contact(self, contact):
        """Findet Email-Adresse für einen Kontakt"""
        company = contact.get('company', '')
        first_name = contact.get('first_name', '')
        last_name = contact.get('last_name', '')
        
        if not company:
            return None
        
        print(f"\n👤 {first_name} {last_name} ({company})")
        
        # 1. Suche Firmen-Website
        domain = self.search_company_website(company)
        
        if not domain:
            print(f"   ❌ Keine Website gefunden")
            return None
        
        # 2. Scrape Website nach Emails
        scraped_emails = self.scrape_website_for_emails(domain)
        
        if scraped_emails:
            print(f"   📧 Gefunden auf Website: {scraped_emails[0]}")
            return scraped_emails[0]
        
        # 3. Generiere Email-Patterns
        generated = self.generate_email_patterns(first_name, last_name, domain)
        
        if generated:
            # Nimm das wahrscheinlichste Pattern (vorname.nachname@domain)
            likely_email = generated[0]
            print(f"   🎯 Generiert: {likely_email}")
            return likely_email
        
        # 4. Fallback auf info@domain
        fallback = f"info@{domain}"
        print(f"   📮 Fallback: {fallback}")
        return fallback
    
    def process_csv(self, input_file='leads.csv', output_file='leads_with_emails.csv'):
        """Verarbeitet die LinkedIn CSV und fügt Emails hinzu"""
        print("\n" + "=" * 60)
        print("📧 EMAIL FINDER - Automatische Email-Suche")
        print("=" * 60)
        
        contacts = []
        
        # Lese CSV
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            contacts = list(reader)
        
        print(f"\n📥 {len(contacts)} Kontakte geladen")
        print("⏳ Starte Email-Suche...\n")
        
        # Finde Emails für jeden Kontakt
        updated_contacts = []
        found_count = 0
        
        for i, contact in enumerate(contacts, 1):
            print(f"[{i}/{len(contacts)}]", end="")
            
            # Finde Email
            email = self.find_email_for_contact(contact)
            
            if email:
                contact['email'] = email
                found_count += 1
            
            updated_contacts.append(contact)
            
            # Kleine Pause zwischen Anfragen
            if i < len(contacts):
                wait = random.uniform(1, 3)
                print(f"   ⏳ Warte {wait:.1f}s...")
                time.sleep(wait)
        
        # Speichere aktualisierte CSV
        if updated_contacts:
            fieldnames = list(updated_contacts[0].keys())
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_contacts)
            
            print("\n" + "=" * 60)
            print("✅ FERTIG!")
            print(f"📊 {found_count}/{len(contacts)} Email-Adressen gefunden")
            print(f"💾 Gespeichert in: {output_file}")
            print("=" * 60)
            
            return output_file
        
        return None

def main():
    print("\n🚀 FutureCheck Email Finder")
    print("Findet automatisch Email-Adressen für deine LinkedIn-Kontakte")
    print("-" * 60)
    
    finder = EmailFinder()
    
    # Optionen
    print("\nWas möchtest du tun?")
    print("1. LinkedIn CSV verarbeiten (leads.csv)")
    print("2. Andere CSV-Datei verarbeiten")
    print("3. Einzelne Email suchen")
    
    choice = input("\nAuswahl (1-3): ").strip()
    
    if choice == '1':
        output = finder.process_csv('leads.csv', 'leads_with_emails.csv')
        if output:
            print(f"\n✅ Fertig! Die Datei '{output}' enthält jetzt Email-Adressen.")
            print("\n📧 Nächste Schritte:")
            print("1. Prüfe die gefundenen Emails")
            print("2. Kopiere leads_with_emails.csv nach ../email-automation/")
            print("3. Starte die Email-Kampagne!")
    
    elif choice == '2':
        input_file = input("CSV-Dateiname: ").strip()
        output_file = input("Output-Dateiname (Enter für 'output_with_emails.csv'): ").strip()
        output_file = output_file or 'output_with_emails.csv'
        
        if input_file:
            output = finder.process_csv(input_file, output_file)
            if output:
                print(f"\n✅ Fertig! Siehe: {output}")
    
    elif choice == '3':
        print("\nKontakt-Details eingeben:")
        first = input("Vorname: ").strip()
        last = input("Nachname: ").strip()
        company = input("Firma: ").strip()
        
        contact = {
            'first_name': first,
            'last_name': last,
            'company': company
        }
        
        email = finder.find_email_for_contact(contact)
        
        if email:
            print(f"\n✅ Email gefunden: {email}")
        else:
            print("\n❌ Keine Email gefunden")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Abgebrochen")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")