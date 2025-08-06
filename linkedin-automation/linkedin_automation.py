#!/usr/bin/env python3
import csv
import json
import sqlite3
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

class LinkedInAutomation:
    def __init__(self, config_path: str = 'config.json', db_path: str = 'database.db'):
        self.config = self.load_config(config_path)
        self.templates = self.load_templates()
        self.db_path = db_path
        self.init_database()
        
    def load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "daily_limit": 50,
            "follow_up_days": [3, 7, 14],
            "industries": ["Handel", "Produktion", "Handwerk", "Dienstleistung"],
            "company_sizes": ["10-50", "50-200", "200-500"]
        }
    
    def load_templates(self, path: str = 'templates.json') -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_templates()
    
    def get_default_templates(self) -> dict:
        return {
            "initial": {
                "Handel": [
                    "Hallo {first_name},\n\nich habe gesehen, dass Sie bei {company} als {position} tätig sind.\n\nViele Handelsunternehmen verlieren aktuell Kunden an Online-Konkurrenten - ohne es rechtzeitig zu merken.\n\nWir analysieren in 24h, wo {company} digital steht und welche 3 Schritte den größten Impact hätten.\n\nHaben Sie 2 Min für ein kurzes Video, das zeigt, was wir genau analysieren?\n\nBeste Grüße\nMarcel",
                    "Guten Tag {first_name},\n\nals {position} bei {company} kennen Sie sicher die Herausforderung: Die Digitalisierung voranzutreiben, ohne dabei das Tagesgeschäft zu vernachlässigen.\n\nUnser FutureCheck zeigt in 24h:\n• Wo Sie im Branchenvergleich stehen\n• Welche Quick-Wins sofort umsetzbar sind\n• Was wirklich ROI bringt\n\nInteresse an einer kostenlosen 5-Min Demo?\n\nViele Grüße\nMarcel"
                ],
                "Produktion": [
                    "Hallo {first_name},\n\nIhre Erfahrung als {position} bei {company} ist sicher wertvoll in Zeiten von Industrie 4.0.\n\nViele Produktionsunternehmen investieren in die falschen Digital-Tools und verlieren dadurch Geld.\n\nUnser FutureCheck analysiert in 24h:\n✓ Digitale Prozesslücken\n✓ Automatisierungspotenziale\n✓ ROI der nächsten Schritte\n\nLust auf eine kurze Demo? Dauert nur 5 Minuten.\n\nBeste Grüße\nMarcel"
                ],
                "default": [
                    "Hallo {first_name},\n\nich habe gesehen, dass Sie bei {company} als {position} tätig sind.\n\nViele Unternehmen Ihrer Größe verlieren aktuell den Anschluss bei der Digitalisierung - oft ohne es zu merken.\n\nWir haben ein Tool entwickelt, das in 24h analysiert, wo Sie stehen und was die wichtigsten nächsten Schritte sind.\n\nHaben Sie 2 Min für ein kurzes Video?\n\nBeste Grüße\nMarcel"
                ]
            },
            "follow_up_1": {
                "default": [
                    "Hallo {first_name},\n\nich wollte nochmal nachfassen zu meiner Nachricht von letzter Woche.\n\nGerade haben wir einem {industry}-Unternehmen geholfen, 30% ihrer Prozesskosten zu sparen.\n\nDie Analyse dauert nur 24h und kostet einmalig 197€ (Early Bird Preis).\n\nSollen wir kurz telefonieren?\n\nBeste Grüße\nMarcel"
                ]
            },
            "follow_up_2": {
                "default": [
                    "Hallo {first_name},\n\nletzte Chance für unseren Early Bird Preis!\n\nNur noch diese Woche: Digitale Reifegradanalyse für 197€ statt 497€.\n\n✓ 30-seitiger Report\n✓ 3 konkrete Handlungsempfehlungen\n✓ ROI-Berechnungen\n✓ 30 Min Beratungsgespräch\n\nHier direkt buchen: zukunfts-check.com\n\nBeste Grüße\nMarcel"
                ]
            }
        }
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                position TEXT,
                company TEXT NOT NULL,
                industry TEXT,
                company_size TEXT,
                linkedin_url TEXT UNIQUE,
                email TEXT,
                status TEXT DEFAULT 'new',
                last_contacted DATE,
                follow_up_count INTEGER DEFAULT 0,
                response_received BOOLEAN DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                message_type TEXT,
                message_text TEXT,
                sent_at TIMESTAMP,
                template_used TEXT,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date DATE,
                end_date DATE,
                total_sent INTEGER DEFAULT 0,
                total_responses INTEGER DEFAULT 0,
                conversion_rate REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def import_leads_from_csv(self, csv_path: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        imported = 0
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO leads 
                        (first_name, last_name, position, company, industry, company_size, linkedin_url, email)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('first_name', ''),
                        row.get('last_name', ''),
                        row.get('position', ''),
                        row.get('company', ''),
                        row.get('industry', ''),
                        row.get('company_size', ''),
                        row.get('linkedin_url', ''),
                        row.get('email', '')
                    ))
                    if cursor.rowcount > 0:
                        imported += 1
                except sqlite3.Error as e:
                    print(f"Error importing lead: {e}")
        
        conn.commit()
        conn.close()
        return imported
    
    def generate_message(self, lead: Dict, message_type: str = 'initial') -> str:
        industry = lead.get('industry', 'default')
        templates_for_industry = self.templates.get(message_type, {}).get(industry)
        
        if not templates_for_industry:
            templates_for_industry = self.templates.get(message_type, {}).get('default', [])
        
        if not templates_for_industry:
            return ""
        
        template = random.choice(templates_for_industry)
        
        message = template.format(
            first_name=lead.get('first_name', 'there'),
            last_name=lead.get('last_name', ''),
            company=lead.get('company', 'Ihrem Unternehmen'),
            position=lead.get('position', 'Ihrer Position'),
            industry=lead.get('industry', 'Ihrer Branche')
        )
        
        return message
    
    def get_leads_to_contact(self, limit: Optional[int] = None) -> List[Dict]:
        if limit is None:
            limit = self.config.get('daily_limit', 50)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM leads 
            WHERE status = 'new' 
            LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        leads = []
        for row in cursor.fetchall():
            leads.append(dict(zip(columns, row)))
        
        conn.close()
        return leads
    
    def get_follow_up_leads(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        follow_up_days = self.config.get('follow_up_days', [3, 7, 14])
        leads = []
        
        for days in follow_up_days:
            target_date = datetime.now() - timedelta(days=days)
            cursor.execute('''
                SELECT * FROM leads 
                WHERE status = 'contacted' 
                AND response_received = 0
                AND last_contacted <= ?
                AND follow_up_count < ?
            ''', (target_date.strftime('%Y-%m-%d'), len(follow_up_days)))
            
            columns = [description[0] for description in cursor.description]
            for row in cursor.fetchall():
                lead = dict(zip(columns, row))
                lead['follow_up_number'] = lead['follow_up_count'] + 1
                leads.append(lead)
        
        conn.close()
        return leads
    
    def mark_as_contacted(self, lead_id: int, message: str, message_type: str = 'initial'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE leads 
            SET status = 'contacted', 
                last_contacted = ?,
                follow_up_count = follow_up_count + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d'), lead_id))
        
        cursor.execute('''
            INSERT INTO messages (lead_id, message_type, message_text, sent_at)
            VALUES (?, ?, ?, ?)
        ''', (lead_id, message_type, message, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def export_campaign_messages(self, output_path: str = 'campaign_messages.csv'):
        leads = self.get_leads_to_contact()
        follow_ups = self.get_follow_up_leads()
        
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['first_name', 'last_name', 'company', 'position', 
                         'linkedin_url', 'message_type', 'message']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for lead in leads:
                message = self.generate_message(lead, 'initial')
                writer.writerow({
                    'first_name': lead['first_name'],
                    'last_name': lead['last_name'],
                    'company': lead['company'],
                    'position': lead['position'],
                    'linkedin_url': lead['linkedin_url'],
                    'message_type': 'initial',
                    'message': message
                })
            
            for lead in follow_ups:
                message_type = f"follow_up_{lead['follow_up_number']}"
                message = self.generate_message(lead, message_type)
                writer.writerow({
                    'first_name': lead['first_name'],
                    'last_name': lead['last_name'],
                    'company': lead['company'],
                    'position': lead['position'],
                    'linkedin_url': lead['linkedin_url'],
                    'message_type': message_type,
                    'message': message
                })
        
        print(f"✅ Exported {len(leads)} initial messages and {len(follow_ups)} follow-ups to {output_path}")
        return len(leads) + len(follow_ups)
    
    def generate_statistics(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM leads')
        total_leads = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'new'")
        new_leads = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'contacted'")
        contacted_leads = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads WHERE response_received = 1")
        responses = cursor.fetchone()[0]
        
        cursor.execute("SELECT industry, COUNT(*) as count FROM leads GROUP BY industry")
        industry_breakdown = cursor.fetchall()
        
        conn.close()
        
        response_rate = (responses / contacted_leads * 100) if contacted_leads > 0 else 0
        
        return {
            'total_leads': total_leads,
            'new_leads': new_leads,
            'contacted_leads': contacted_leads,
            'responses': responses,
            'response_rate': f"{response_rate:.1f}%",
            'industry_breakdown': dict(industry_breakdown)
        }

def main():
    automation = LinkedInAutomation()
    
    print("🚀 FutureCheck LinkedIn Automation Tool")
    print("=" * 50)
    
    while True:
        print("\nWas möchtest du tun?")
        print("1. Leads aus CSV importieren")
        print("2. Nachrichten für heute generieren")
        print("3. Statistiken anzeigen")
        print("4. Kampagne exportieren")
        print("5. Beenden")
        
        choice = input("\nAuswahl (1-5): ")
        
        if choice == '1':
            csv_path = input("CSV-Dateipfad (oder Enter für 'leads.csv'): ").strip() or 'leads.csv'
            if os.path.exists(csv_path):
                count = automation.import_leads_from_csv(csv_path)
                print(f"✅ {count} neue Leads importiert!")
            else:
                print(f"❌ Datei {csv_path} nicht gefunden!")
        
        elif choice == '2':
            limit = input("Wie viele Nachrichten? (Enter für Standard): ").strip()
            limit = int(limit) if limit else None
            leads = automation.get_leads_to_contact(limit)
            
            print(f"\n📬 Generiere Nachrichten für {len(leads)} Leads:")
            for lead in leads[:5]:
                message = automation.generate_message(lead)
                print(f"\n👤 {lead['first_name']} {lead['last_name']} ({lead['company']})")
                print("-" * 40)
                print(message[:200] + "..." if len(message) > 200 else message)
        
        elif choice == '3':
            stats = automation.generate_statistics()
            print("\n📊 Kampagnen-Statistiken:")
            print(f"Total Leads: {stats['total_leads']}")
            print(f"Neue Leads: {stats['new_leads']}")
            print(f"Kontaktiert: {stats['contacted_leads']}")
            print(f"Antworten: {stats['responses']}")
            print(f"Response Rate: {stats['response_rate']}")
            print("\nBranchen-Verteilung:")
            for industry, count in stats['industry_breakdown'].items():
                print(f"  {industry}: {count}")
        
        elif choice == '4':
            output_file = input("Output-Dateiname (Enter für 'campaign_messages.csv'): ").strip() or 'campaign_messages.csv'
            count = automation.export_campaign_messages(output_file)
            print(f"✅ {count} Nachrichten exportiert nach {output_file}")
        
        elif choice == '5':
            print("👋 Auf Wiedersehen!")
            break
        
        else:
            print("❌ Ungültige Auswahl!")

if __name__ == "__main__":
    main()