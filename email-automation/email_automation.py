#!/usr/bin/env python3
import csv
import json
import sqlite3
import smtplib
import ssl
import time
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import hashlib

class EmailAutomation:
    def __init__(self, config_path: str = 'email_config.json', db_path: str = 'email_database.db'):
        self.config = self.load_config(config_path)
        self.templates = self.load_templates()
        self.db_path = db_path
        self.init_database()
        
    def load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self) -> dict:
        return {
            "smtp": {
                "server": "smtp.gmail.com",
                "port": 587,
                "use_tls": True,
                "email": "",
                "password": "",
                "from_name": "Marcel von FutureCheck"
            },
            "campaign": {
                "daily_limit": 100,
                "hourly_limit": 20,
                "sequence_delays": [0, 2, 5, 7, 14, 21, 30],
                "business_hours_only": True,
                "working_hours": {"start": "09:00", "end": "17:00"},
                "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            },
            "tracking": {
                "track_opens": True,
                "track_clicks": True,
                "tracking_domain": "track.zukunfts-check.com"
            }
        }
    
    def load_templates(self, path: str = 'email_templates.json') -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                company TEXT,
                position TEXT,
                industry TEXT,
                company_size TEXT,
                phone TEXT,
                website TEXT,
                source TEXT,
                status TEXT DEFAULT 'new',
                score INTEGER DEFAULT 0,
                tags TEXT,
                unsubscribed BOOLEAN DEFAULT 0,
                bounced BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails_sent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                campaign_id INTEGER,
                sequence_number INTEGER,
                subject TEXT,
                body TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                opened BOOLEAN DEFAULT 0,
                opened_at TIMESTAMP,
                clicked BOOLEAN DEFAULT 0,
                clicked_at TIMESTAMP,
                replied BOOLEAN DEFAULT 0,
                replied_at TIMESTAMP,
                tracking_id TEXT UNIQUE,
                FOREIGN KEY (contact_id) REFERENCES contacts(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'draft',
                start_date DATE,
                end_date DATE,
                total_contacts INTEGER DEFAULT 0,
                emails_sent INTEGER DEFAULT 0,
                opens INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                unsubscribes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                campaign_id INTEGER,
                sequence_number INTEGER,
                scheduled_for TIMESTAMP,
                status TEXT DEFAULT 'pending',
                attempts INTEGER DEFAULT 0,
                last_error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contact_id) REFERENCES contacts(id),
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def import_contacts_from_csv(self, csv_path: str) -> Tuple[int, int]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        imported = 0
        skipped = 0
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row.get('email', '').strip().lower()
                
                if not self.validate_email(email):
                    skipped += 1
                    continue
                
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO contacts 
                        (email, first_name, last_name, company, position, industry, 
                         company_size, phone, website, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        email,
                        row.get('first_name', ''),
                        row.get('last_name', ''),
                        row.get('company', ''),
                        row.get('position', ''),
                        row.get('industry', ''),
                        row.get('company_size', ''),
                        row.get('phone', ''),
                        row.get('website', ''),
                        row.get('source', 'csv_import')
                    ))
                    if cursor.rowcount > 0:
                        imported += 1
                    else:
                        skipped += 1
                except sqlite3.Error as e:
                    print(f"Error importing contact: {e}")
                    skipped += 1
        
        conn.commit()
        conn.close()
        return imported, skipped
    
    def validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def create_campaign(self, name: str, description: str = "") -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO campaigns (name, description, status, start_date)
            VALUES (?, ?, 'active', ?)
        ''', (name, description, datetime.now()))
        
        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return campaign_id
    
    def add_contacts_to_campaign(self, campaign_id: int, contact_ids: List[int] = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if contact_ids is None:
            cursor.execute('''
                SELECT id FROM contacts 
                WHERE status = 'new' 
                AND unsubscribed = 0 
                AND bounced = 0
            ''')
            contact_ids = [row[0] for row in cursor.fetchall()]
        
        for contact_id in contact_ids:
            for seq_num, delay_days in enumerate(self.config['campaign']['sequence_delays']):
                scheduled_time = datetime.now() + timedelta(days=delay_days)
                
                cursor.execute('''
                    INSERT INTO email_queue 
                    (contact_id, campaign_id, sequence_number, scheduled_for)
                    VALUES (?, ?, ?, ?)
                ''', (contact_id, campaign_id, seq_num, scheduled_time))
        
        cursor.execute('''
            UPDATE campaigns 
            SET total_contacts = ? 
            WHERE id = ?
        ''', (len(contact_ids), campaign_id))
        
        conn.commit()
        conn.close()
        
        return len(contact_ids)
    
    def generate_email_content(self, contact: Dict, sequence_number: int) -> Tuple[str, str, str]:
        templates = self.templates.get('sequences', [])
        
        if sequence_number >= len(templates):
            sequence_number = len(templates) - 1
        
        template = templates[sequence_number] if templates else self.get_default_template(sequence_number)
        
        subject = template['subject'].format(
            first_name=contact.get('first_name', 'there'),
            company=contact.get('company', 'Ihr Unternehmen'),
            industry=contact.get('industry', 'Ihre Branche')
        )
        
        text_body = template['text'].format(
            first_name=contact.get('first_name', 'there'),
            last_name=contact.get('last_name', ''),
            company=contact.get('company', 'Ihr Unternehmen'),
            position=contact.get('position', 'Ihre Position'),
            industry=contact.get('industry', 'Ihre Branche')
        )
        
        tracking_id = self.generate_tracking_id(contact['email'], sequence_number)
        
        html_body = self.create_html_email(text_body, tracking_id)
        
        return subject, text_body, html_body
    
    def get_default_template(self, sequence_number: int) -> dict:
        templates = [
            {
                "subject": "🚀 {company} - Digitaler Reifegrad in 24h erfahren",
                "text": """Hallo {first_name},

wussten Sie, dass 67% der KMU nicht wissen, wo sie bei der Digitalisierung stehen?

{company} könnte in nur 24 Stunden Klarheit haben:
✓ Digitaler Reifegrad Score (0-100)
✓ Vergleich mit Ihrer Branche
✓ 3 konkrete nächste Schritte

Aktuell zum Early-Bird Preis: 197€ statt 497€

Interesse? Einfach auf diesen Link klicken:
https://zukunfts-check.com

Beste Grüße
Marcel Gärtner
FutureCheck Gründer"""
            },
            {
                "subject": "Re: {company} - Haben Sie 2 Minuten?",
                "text": """Hallo {first_name},

kurze Nachfrage zu meiner Email von vor 2 Tagen.

Gerade haben wir einem {industry}-Unternehmen geholfen, 
ihre digitalen Schwachstellen zu identifizieren.

Das Ergebnis: 30% Effizienzsteigerung in 6 Monaten.

Für {company} könnte das auch interessant sein.

Hier gibt's mehr Infos (2 Min Video):
https://zukunfts-check.com

Beste Grüße
Marcel"""
            },
            {
                "subject": "💡 {first_name}, Case Study aus Ihrer Branche",
                "text": """Hallo {first_name},

möchte Sie nicht nerven, aber das könnte interessant sein:

Ein {industry}-Unternehmen (150 Mitarbeiter) hat nach 
unserem FutureCheck folgendes erreicht:

• 40% weniger manuelle Prozesse
• 25% mehr Online-Umsatz
• 50% schnellere Auftragsabwicklung

Die Analyse hat 24h gedauert und 197€ gekostet.
Der ROI lag bei 2.400% im ersten Jahr.

Details hier: https://zukunfts-check.com

Viele Grüße
Marcel

PS: Nur noch 8 Early-Bird Plätze verfügbar!"""
            }
        ]
        
        if sequence_number < len(templates):
            return templates[sequence_number]
        return templates[-1]
    
    def create_html_email(self, text_content: str, tracking_id: str) -> str:
        text_lines = text_content.split('\n')
        html_content = []
        
        for line in text_lines:
            if line.startswith('http'):
                line = f'<a href="{line}?tid={tracking_id}" style="color: #007bff;">{line}</a>'
            elif line.startswith('•') or line.startswith('✓'):
                line = f'<li>{line[1:].strip()}</li>'
            elif line == '':
                line = '<br>'
            else:
                line = f'<p>{line}</p>'
            html_content.append(line)
        
        tracking_pixel = f'<img src="https://track.zukunfts-check.com/open?tid={tracking_id}" width="1" height="1" />'
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                p {{ margin: 10px 0; }}
                a {{ color: #007bff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .signature {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
                .footer {{ margin-top: 50px; padding: 20px; background: #f8f9fa; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            {''.join(html_content)}
            
            <div class="signature">
                <p><strong>Marcel Gärtner</strong><br>
                Gründer & CEO<br>
                FutureCheck - Digital Maturity Assessment<br>
                📧 marcel@zukunfts-check.com<br>
                📱 +49 170 123 4567<br>
                🌐 <a href="https://zukunfts-check.com">zukunfts-check.com</a></p>
            </div>
            
            <div class="footer">
                <p>Sie erhalten diese Email, weil Ihre Firma für unseren Service relevant ist.<br>
                <a href="https://zukunfts-check.com">Hier abmelden</a> | 
                <a href="https://zukunfts-check.com">Datenschutz</a></p>
            </div>
            {tracking_pixel}
        </body>
        </html>
        """
        
        return html_template
    
    def generate_tracking_id(self, email: str, sequence: int) -> str:
        data = f"{email}_{sequence}_{datetime.now().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:16]
    
    def send_email(self, to_email: str, subject: str, text_body: str, html_body: str) -> bool:
        smtp_config = self.config['smtp']
        
        if not smtp_config['email'] or not smtp_config['password']:
            print("❌ SMTP Zugangsdaten fehlen in email_config.json!")
            return False
        
        message = MIMEMultipart('alternative')
        message['From'] = f"{smtp_config['from_name']} <{smtp_config['email']}>"
        message['To'] = to_email
        message['Subject'] = subject
        message['Reply-To'] = smtp_config['email']
        
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
            print(f"❌ Fehler beim Email-Versand: {e}")
            return False
    
    def process_email_queue(self, limit: int = None):
        if limit is None:
            limit = self.config['campaign']['hourly_limit']
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT q.id, q.contact_id, q.campaign_id, q.sequence_number, c.*
            FROM email_queue q
            JOIN contacts c ON q.contact_id = c.id
            WHERE q.status = 'pending'
            AND q.scheduled_for <= ?
            AND c.unsubscribed = 0
            AND c.bounced = 0
            ORDER BY q.scheduled_for
            LIMIT ?
        ''', (datetime.now(), limit))
        
        columns = [description[0] for description in cursor.description]
        queue_items = []
        for row in cursor.fetchall():
            queue_items.append(dict(zip(columns, row)))
        
        sent_count = 0
        failed_count = 0
        
        for item in queue_items:
            contact = {
                'email': item['email'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'company': item['company'],
                'position': item['position'],
                'industry': item['industry']
            }
            
            subject, text_body, html_body = self.generate_email_content(
                contact, 
                item['sequence_number']
            )
            
            if self.send_email(contact['email'], subject, text_body, html_body):
                cursor.execute('''
                    UPDATE email_queue 
                    SET status = 'sent' 
                    WHERE id = ?
                ''', (item['id'],))
                
                tracking_id = self.generate_tracking_id(
                    contact['email'], 
                    item['sequence_number']
                )
                
                cursor.execute('''
                    INSERT INTO emails_sent 
                    (contact_id, campaign_id, sequence_number, subject, body, tracking_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    item['contact_id'],
                    item['campaign_id'],
                    item['sequence_number'],
                    subject,
                    text_body,
                    tracking_id
                ))
                
                cursor.execute('''
                    UPDATE contacts 
                    SET status = 'contacted' 
                    WHERE id = ?
                ''', (item['contact_id'],))
                
                sent_count += 1
                print(f"✅ Email gesendet an: {contact['email']}")
                
                time.sleep(random.randint(5, 15))
            else:
                cursor.execute('''
                    UPDATE email_queue 
                    SET attempts = attempts + 1,
                        last_error = 'Send failed'
                    WHERE id = ?
                ''', (item['id'],))
                failed_count += 1
        
        conn.commit()
        conn.close()
        
        return sent_count, failed_count
    
    def get_campaign_stats(self, campaign_id: int = None) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if campaign_id:
            cursor.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
        else:
            cursor.execute('SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 1')
        
        campaign = cursor.fetchone()
        
        if not campaign:
            return {}
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_sent,
                SUM(opened) as total_opened,
                SUM(clicked) as total_clicked,
                SUM(replied) as total_replied
            FROM emails_sent
            WHERE campaign_id = ?
        ''', (campaign[0],))
        
        stats = cursor.fetchone()
        
        conn.close()
        
        total_sent = stats[0] or 0
        total_opened = stats[1] or 0
        total_clicked = stats[2] or 0
        total_replied = stats[3] or 0
        
        return {
            'campaign_name': campaign[1],
            'total_contacts': campaign[5],
            'total_sent': total_sent,
            'total_opened': total_opened,
            'total_clicked': total_clicked,
            'total_replied': total_replied,
            'open_rate': f"{(total_opened/total_sent*100):.1f}%" if total_sent > 0 else "0%",
            'click_rate': f"{(total_clicked/total_sent*100):.1f}%" if total_sent > 0 else "0%",
            'reply_rate': f"{(total_replied/total_sent*100):.1f}%" if total_sent > 0 else "0%"
        }
    
    def export_campaign_data(self, output_path: str = 'email_campaign_export.csv'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.email,
                c.first_name,
                c.last_name,
                c.company,
                c.status,
                COUNT(e.id) as emails_sent,
                SUM(e.opened) as times_opened,
                SUM(e.clicked) as times_clicked,
                SUM(e.replied) as replied
            FROM contacts c
            LEFT JOIN emails_sent e ON c.id = e.contact_id
            GROUP BY c.id
        ''')
        
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Email', 'First Name', 'Last Name', 'Company', 
                'Status', 'Emails Sent', 'Opens', 'Clicks', 'Replied'
            ])
            
            for row in cursor.fetchall():
                writer.writerow(row)
        
        conn.close()
        print(f"✅ Daten exportiert nach: {output_path}")

def main():
    automation = EmailAutomation()
    
    print("📧 FutureCheck Email Automation System")
    print("=" * 50)
    
    while True:
        print("\n📋 HAUPTMENÜ:")
        print("1. 📥 Kontakte importieren (CSV)")
        print("2. 🚀 Neue Kampagne starten")
        print("3. 📤 Emails versenden (Queue abarbeiten)")
        print("4. 📊 Kampagnen-Statistiken")
        print("5. 💾 Daten exportieren")
        print("6. ⚙️  SMTP einrichten")
        print("7. 🚪 Beenden")
        
        choice = input("\nAuswahl (1-7): ")
        
        if choice == '1':
            csv_path = input("CSV-Dateipfad (Enter für 'email_contacts.csv'): ").strip()
            csv_path = csv_path or 'email_contacts.csv'
            
            if os.path.exists(csv_path):
                imported, skipped = automation.import_contacts_from_csv(csv_path)
                print(f"✅ {imported} Kontakte importiert")
                print(f"⚠️  {skipped} übersprungen (Duplikate/Fehler)")
            else:
                print(f"❌ Datei nicht gefunden: {csv_path}")
        
        elif choice == '2':
            name = input("Kampagnen-Name: ")
            desc = input("Beschreibung (optional): ")
            
            campaign_id = automation.create_campaign(name, desc)
            print(f"✅ Kampagne '{name}' erstellt (ID: {campaign_id})")
            
            add_all = input("Alle neuen Kontakte hinzufügen? (j/n): ")
            if add_all.lower() == 'j':
                count = automation.add_contacts_to_campaign(campaign_id)
                print(f"✅ {count} Kontakte zur Kampagne hinzugefügt")
        
        elif choice == '3':
            limit = input("Wie viele Emails senden? (Enter für Standard): ").strip()
            limit = int(limit) if limit else None
            
            print("\n📤 Versende Emails...")
            sent, failed = automation.process_email_queue(limit)
            print(f"✅ {sent} Emails erfolgreich versendet")
            if failed > 0:
                print(f"❌ {failed} Emails fehlgeschlagen")
        
        elif choice == '4':
            stats = automation.get_campaign_stats()
            if stats:
                print(f"\n📊 Kampagne: {stats['campaign_name']}")
                print(f"Kontakte: {stats['total_contacts']}")
                print(f"Versendet: {stats['total_sent']}")
                print(f"Öffnungsrate: {stats['open_rate']}")
                print(f"Klickrate: {stats['click_rate']}")
                print(f"Antwortrate: {stats['reply_rate']}")
            else:
                print("❌ Keine Kampagne gefunden")
        
        elif choice == '5':
            output = input("Export-Dateiname (Enter für 'email_campaign_export.csv'): ").strip()
            output = output or 'email_campaign_export.csv'
            automation.export_campaign_data(output)
        
        elif choice == '6':
            print("\n⚙️  SMTP Konfiguration")
            print("Bearbeite email_config.json mit deinen Zugangsdaten:")
            print('  "email": "deine-email@gmail.com"')
            print('  "password": "dein-app-passwort"')
            print("\nFür Gmail: https://support.google.com/accounts/answer/185833")
        
        elif choice == '7':
            print("👋 Auf Wiedersehen!")
            break

if __name__ == "__main__":
    main()