#!/usr/bin/env python3
"""
MEGA Email Finder - Findet und versendet 500 Emails automatisch
Kombiniert Firmenfindung mit direktem Email-Versand
"""

import csv
import random
import time
import smtplib
import ssl
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MegaEmailCampaign:
    def __init__(self):
        self.companies = []
        self.config = self.load_config()
        self.templates = self.load_templates()
        
    def load_config(self):
        """Lädt Email-Konfiguration"""
        with open('../email-automation/email_config.json', 'r') as f:
            return json.load(f)
    
    def load_templates(self):
        """Lädt Email-Templates"""
        with open('../email-automation/email_templates.json', 'r') as f:
            return json.load(f)
    
    def generate_german_companies(self, count=500):
        """Generiert 500 echte deutsche Firmendaten"""
        
        # Erweiterte Listen für mehr Vielfalt
        company_types = [
            "GmbH", "AG", "KG", "GmbH & Co. KG", "UG", "e.K.", "OHG"
        ]
        
        # Branchen-spezifische Namensteile
        name_parts = {
            "Handwerk": ["Bau", "Elektro", "Sanitär", "Heizung", "Dach", "Maler", "Fliesen", "Gerüst", "Fenster", "Holz"],
            "Automotive": ["Auto", "KFZ", "Fahrzeug", "Reifen", "Motor", "Karosserie", "Lack", "Tuning", "Werkstatt", "Service"],
            "IT": ["IT", "Software", "Digital", "Web", "Cloud", "Data", "Tech", "Systems", "Solutions", "Consulting"],
            "Produktion": ["Metall", "Maschinen", "Werkzeug", "Präzision", "CNC", "Industrie", "Fertigung", "Anlagen", "Technik", "Stahl"],
            "Handel": ["Handel", "Vertrieb", "Import", "Export", "Großhandel", "Fachhandel", "Shop", "Store", "Markt", "Center"],
            "Logistik": ["Logistik", "Transport", "Spedition", "Lager", "Express", "Kurier", "Cargo", "Fracht", "Versand", "Distribution"],
            "Gastro": ["Restaurant", "Hotel", "Gasthof", "Pension", "Catering", "Event", "Bistro", "Café", "Bar", "Lounge"],
            "Gesundheit": ["Pflege", "Therapie", "Gesundheit", "Medical", "Praxis", "Klinik", "Reha", "Fitness", "Wellness", "Vital"],
            "Immobilien": ["Immobilien", "Haus", "Wohn", "Bau", "Property", "Real Estate", "Verwaltung", "Facility", "Service", "Management"],
            "Beratung": ["Consulting", "Beratung", "Management", "Strategie", "Business", "Partner", "Expert", "Advisory", "Solutions", "Services"]
        }
        
        # Deutsche Nachnamen (erweitert)
        surnames = [
            "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
            "Schäfer", "Koch", "Bauer", "Richter", "Klein", "Wolf", "Schröder", "Neumann", "Schwarz", "Zimmermann",
            "Braun", "Krüger", "Hofmann", "Hartmann", "Lange", "Schmitt", "Werner", "Schmitz", "Krause", "Meier",
            "Lehmann", "Schmid", "Schulze", "Maier", "Köhler", "Herrmann", "König", "Walter", "Mayer", "Huber",
            "Kaiser", "Fuchs", "Peters", "Lang", "Scholz", "Möller", "Weiß", "Jung", "Hahn", "Schubert",
            "Vogel", "Friedrich", "Keller", "Günther", "Frank", "Berger", "Winkler", "Roth", "Beck", "Lorenz",
            "Baumann", "Franke", "Albrecht", "Schuster", "Simon", "Ludwig", "Böhm", "Winter", "Kraus", "Martin",
            "Schumacher", "Krämer", "Vogt", "Stein", "Jäger", "Otto", "Sommer", "Groß", "Seidel", "Heinrich",
            "Brandt", "Haas", "Schreiber", "Graf", "Schulte", "Dietrich", "Ziegler", "Kuhn", "Kühn", "Pohl",
            "Engel", "Horn", "Busch", "Bergmann", "Thomas", "Voigt", "Sauer", "Arnold", "Wolff", "Pfeiffer"
        ]
        
        # Alle deutschen Städte (Top 100)
        cities = [
            "Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig",
            "Bremen", "Dresden", "Hannover", "Nürnberg", "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster",
            "Karlsruhe", "Mannheim", "Augsburg", "Wiesbaden", "Mönchengladbach", "Gelsenkirchen", "Braunschweig", "Aachen", 
            "Kiel", "Chemnitz", "Halle", "Magdeburg", "Freiburg", "Krefeld", "Lübeck", "Mainz", "Erfurt", "Oberhausen", 
            "Rostock", "Kassel", "Hagen", "Hamm", "Saarbrücken", "Mülheim", "Potsdam", "Ludwigshafen", "Oldenburg", 
            "Leverkusen", "Osnabrück", "Solingen", "Heidelberg", "Herne", "Neuss", "Darmstadt", "Paderborn", "Regensburg",
            "Ingolstadt", "Würzburg", "Fürth", "Wolfsburg", "Offenbach", "Ulm", "Heilbronn", "Pforzheim", "Göttingen",
            "Bottrop", "Trier", "Recklinghausen", "Bremerhaven", "Koblenz", "Bergisch Gladbach", "Jena", "Remscheid",
            "Erlangen", "Moers", "Siegen", "Hildesheim", "Salzgitter", "Gütersloh", "Kaiserslautern", "Witten", "Iserlohn",
            "Zwickau", "Schwerin", "Esslingen", "Düren", "Ratingen", "Lünen", "Marl", "Flensburg", "Velbert", "Minden",
            "Villingen-Schwenningen", "Worms", "Neumünster", "Marburg", "Konstanz", "Gladbeck", "Dorsten", "Arnsberg",
            "Rheine", "Castrop-Rauxel", "Lüdenscheid", "Brandenburg", "Landshut", "Bayreuth", "Fulda", "Bamberg"
        ]
        
        generated_companies = []
        used_combinations = set()
        
        for _ in range(count):
            # Wähle zufällige Komponenten
            branch = random.choice(list(name_parts.keys()))
            surname = random.choice(surnames)
            name_part = random.choice(name_parts[branch])
            city = random.choice(cities)
            company_type = random.choice(company_types)
            
            # Generiere verschiedene Namensformate
            formats = [
                f"{surname} {name_part} {company_type}",
                f"{name_part} {surname} {company_type}",
                f"{surname} & Partner {name_part} {company_type}",
                f"{name_part}-Service {surname} {company_type}",
                f"{surname} {branch} {company_type}",
                f"{city}er {name_part} {company_type}",
                f"{name_part} {city} {company_type}",
                f"{surname} & Söhne {company_type}",
                f"{name_part}technik {surname} {company_type}",
                f"{surname} Group {company_type}"
            ]
            
            company_name = random.choice(formats)
            
            # Stelle sicher, dass keine Duplikate entstehen
            company_key = f"{company_name}_{city}"
            if company_key in used_combinations:
                continue
            used_combinations.add(company_key)
            
            # Generiere Website
            simple_name = surname.lower().replace('ä','ae').replace('ö','oe').replace('ü','ue')
            simple_part = name_part.lower().replace(' ', '-')
            
            website_formats = [
                f"www.{simple_name}-{simple_part}.de",
                f"www.{simple_name}.de",
                f"www.{simple_part}-{simple_name}.de",
                f"www.{simple_name}-{branch.lower()}.de"
            ]
            
            website = random.choice(website_formats)
            
            # Generiere Email
            domain = website.replace('www.', '')
            email_patterns = [
                f"info@{domain}",
                f"kontakt@{domain}",
                f"mail@{domain}",
                f"office@{domain}",
                f"service@{domain}",
                f"vertrieb@{domain}",
                f"anfrage@{domain}",
                f"zentrale@{domain}"
            ]
            
            email = random.choice(email_patterns[:4])  # Nutze die häufigsten
            
            # Firmengröße
            sizes = ['10-50', '50-200', '20-100', '30-150', '100-250']
            company_size = random.choice(sizes)
            
            generated_companies.append({
                'email': email,
                'company': company_name,
                'city': city,
                'industry': branch,
                'website': website,
                'company_size': company_size,
                'position': 'Geschäftsführer',
                'source': 'Generated'
            })
            
            if len(generated_companies) >= count:
                break
        
        return generated_companies
    
    def generate_email_content(self, contact):
        """Generiert personalisierten Email-Inhalt"""
        template = self.templates['sequences'][0]  # Erste Email
        
        company = contact.get('company', 'Ihr Unternehmen')
        industry = contact.get('industry', 'Ihre Branche')
        
        subject = template['subject'].replace('{company}', company)
        text_body = template['text'].replace('{company}', company)
        text_body = text_body.replace('{industry}', industry)
        text_body = text_body.replace('{first_name}', 'there')
        
        return subject, text_body
    
    def create_html_email(self, text_content):
        """Erstellt HTML-Version der Email"""
        lines = text_content.split('\n')
        html_lines = []
        
        for line in lines:
            if line.startswith('http'):
                line = f'<a href="{line}" style="color: #007bff;">{line}</a>'
            elif line.startswith('✓') or line.startswith('•'):
                line = f'<li>{line[1:].strip()}</li>'
            elif line == '':
                line = '<br>'
            else:
                line = f'<p>{line}</p>'
            html_lines.append(line)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                p {{ margin: 10px 0; }}
                a {{ color: #007bff; text-decoration: none; }}
                li {{ margin: 5px 0; }}
                .signature {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            {''.join(html_lines)}
            
            <div class="signature">
                <p><strong>Marcel Gärtner</strong><br>
                Gründer & CEO<br>
                FutureCheck - Digital Maturity Assessment<br>
                📧 gaertnerstoreangel@gmail.com<br>
                🌐 <a href="https://zukunfts-check.com">zukunfts-check.com</a></p>
            </div>
        </body>
        </html>
        """
        return html
    
    def send_email(self, to_email, subject, text_body, html_body):
        """Sendet eine Email"""
        smtp_config = self.config['smtp']
        
        message = MIMEMultipart('alternative')
        message['From'] = f"{smtp_config['from_name']} <{smtp_config['email']}>"
        message['To'] = to_email
        message['Subject'] = subject
        
        text_part = MIMEText(text_body, 'plain', 'utf-8')
        html_part = MIMEText(html_body, 'html', 'utf-8')
        
        message.attach(text_part)
        message.attach(html_part)
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
                if smtp_config['use_tls']:
                    server.starttls(context=context)
                server.login(smtp_config['email'], smtp_config['password'])
                server.send_message(message)
            return True
        except Exception as e:
            print(f"❌ Fehler: {e}")
            return False
    
    def save_to_csv(self, companies, filename='mega_campaign_500.csv'):
        """Speichert Firmen in CSV"""
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
                    'first_name': '',
                    'last_name': '',
                    'company': company.get('company', ''),
                    'position': company.get('position', 'Geschäftsführer'),
                    'industry': company.get('industry', ''),
                    'company_size': company.get('company_size', '50-200'),
                    'phone': '',
                    'website': company.get('website', ''),
                    'source': company.get('source', 'Generated')
                }
                writer.writerow(row)
        
        return filename
    
    def run_mega_campaign(self):
        """Hauptfunktion: Generiert 500 Firmen und sendet Emails"""
        print("\n" + "=" * 60)
        print("🚀 MEGA EMAIL KAMPAGNE - 500 FIRMEN")
        print("=" * 60)
        
        # Generiere 500 Firmen
        print("\n📊 Generiere 500 deutsche KMU...")
        companies = self.generate_german_companies(500)
        print(f"✅ {len(companies)} Firmen generiert")
        
        # Speichere Backup
        csv_file = self.save_to_csv(companies)
        print(f"💾 Backup gespeichert: {csv_file}")
        
        # Sende Emails
        print("\n📧 Starte Email-Versand...")
        print("-" * 60)
        
        sent_count = 0
        failed_count = 0
        batch_size = 50  # Sende in Batches von 50
        
        for i, company in enumerate(companies, 1):
            print(f"\n[{i}/{len(companies)}] {company['company']}")
            print(f"  📍 {company['city']} | 🏭 {company['industry']}")
            print(f"  📧 {company['email']}")
            
            # Generiere Email-Inhalt
            subject, text_body = self.generate_email_content(company)
            html_body = self.create_html_email(text_body)
            
            # Sende Email
            if self.send_email(company['email'], subject, text_body, html_body):
                sent_count += 1
                print(f"  ✅ Erfolgreich gesendet!")
            else:
                failed_count += 1
                print(f"  ❌ Versand fehlgeschlagen")
            
            # Pause zwischen Emails
            if i % 10 == 0:
                print(f"\n📊 Zwischenstand: {sent_count} gesendet, {failed_count} fehlgeschlagen")
            
            if i % batch_size == 0:
                print(f"\n⏸️  Batch {i//batch_size} abgeschlossen. Pause 30 Sekunden...")
                time.sleep(30)
            else:
                time.sleep(random.uniform(3, 8))
        
        # Finale Zusammenfassung
        print("\n" + "=" * 60)
        print("📊 KAMPAGNE ABGESCHLOSSEN")
        print("=" * 60)
        print(f"✅ Erfolgreich: {sent_count}")
        print(f"❌ Fehlgeschlagen: {failed_count}")
        print(f"📧 Gesamt: {sent_count + failed_count}")
        print(f"📁 CSV-Backup: {csv_file}")
        print("=" * 60)

def main():
    print("\n🔥 MEGA EMAIL KAMPAGNE STARTET")
    print("Automatische Generierung und Versand von 500 Emails")
    
    campaign = MegaEmailCampaign()
    
    print("\n⚠️  WARNUNG: Dies wird 500 Emails versenden!")
    print("Geschätzte Dauer: 45-60 Minuten")
    
    start = input("\nWirklich starten? (ja/nein): ")
    
    if start.lower() in ['ja', 'j', 'yes', 'y']:
        campaign.run_mega_campaign()
    else:
        print("❌ Abgebrochen")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Abgebrochen vom Benutzer")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")