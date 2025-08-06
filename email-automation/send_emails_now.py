#!/usr/bin/env python3
"""
Quick-Fix Script: Sendet Emails direkt ohne Queue-Probleme
"""

import csv
import json
import smtplib
import ssl
import time
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_config():
    with open('email_config.json', 'r') as f:
        return json.load(f)

def load_templates():
    with open('email_templates.json', 'r') as f:
        return json.load(f)

def load_contacts(limit=5, skip=0):
    contacts = []
    with open('deutsche_firmen_70_20250806_012533.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < skip:
                continue
            if i >= skip + limit:
                break
            contacts.append(row)
    return contacts

def generate_email_content(contact, templates):
    template = templates['sequences'][0]  # Erste Email der Sequenz
    
    # Personalisierung
    first_name = contact.get('first_name', 'there')
    company = contact.get('company', 'Ihr Unternehmen')
    industry = contact.get('industry', 'Ihre Branche')
    position = contact.get('position', 'Ihre Position')
    
    subject = template['subject'].replace('{company}', company)
    subject = subject.replace('{first_name}', first_name)
    
    text_body = template['text'].replace('{first_name}', first_name)
    text_body = text_body.replace('{company}', company)
    text_body = text_body.replace('{industry}', industry)
    text_body = text_body.replace('{position}', position)
    
    return subject, text_body

def create_html_email(text_content):
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
            a:hover {{ text-decoration: underline; }}
            li {{ margin: 5px 0; }}
            .signature {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
            .footer {{ margin-top: 50px; padding: 20px; background: #f8f9fa; text-align: center; font-size: 12px; color: #666; }}
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
        
        <div class="footer">
            <p>Sie erhalten diese Email, weil Ihre Firma für unseren Service relevant ist.<br>
            <a href="https://zukunfts-check.com">Abmelden</a> | 
            <a href="https://zukunfts-check.com">Datenschutz</a></p>
        </div>
    </body>
    </html>
    """
    return html

def send_email(config, to_email, subject, text_body, html_body):
    smtp_config = config['smtp']
    
    message = MIMEMultipart('alternative')
    message['From'] = f"{smtp_config['from_name']} <{smtp_config['email']}>"
    message['To'] = to_email
    message['Subject'] = subject
    message['Reply-To'] = smtp_config['reply_to']
    
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
        print(f"❌ Fehler beim Versand an {to_email}: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("📧 FUTURECHECK DIRECT EMAIL SENDER")
    print("=" * 60)
    
    # Konfiguration laden
    config = load_config()
    templates = load_templates()
    
    # Anzahl der Emails abfragen
    num_emails = input("\nWie viele Emails senden? (Enter für 5): ").strip()
    num_emails = int(num_emails) if num_emails else 5
    
    # Skip-Parameter abfragen
    skip_contacts = input("Wie viele Kontakte überspringen? (Enter für 0): ").strip()
    skip_contacts = int(skip_contacts) if skip_contacts else 0
    
    # Test-Modus?
    test_mode = input("Test-Modus? (Alle Emails an dich selbst) (j/n): ").strip()
    test_email = config['smtp']['email'] if test_mode.lower() == 'j' else None
    
    # Kontakte laden
    print(f"\n📥 Lade {num_emails} Kontakte (überspringe {skip_contacts})...")
    contacts = load_contacts(num_emails, skip_contacts)
    
    if not contacts:
        print("❌ Keine Kontakte gefunden!")
        return
    
    print(f"✅ {len(contacts)} Kontakte geladen\n")
    
    # Emails versenden
    sent_count = 0
    failed_count = 0
    
    print("📤 Starte Email-Versand...\n")
    print("-" * 60)
    
    for i, contact in enumerate(contacts, 1):
        # Email-Inhalt generieren
        subject, text_body = generate_email_content(contact, templates)
        html_body = create_html_email(text_body)
        
        # Empfänger bestimmen
        recipient = test_email if test_email else contact.get('email')
        
        # Info ausgeben
        print(f"\n[{i}/{len(contacts)}] Sende an: {recipient}")
        print(f"    Firma: {contact.get('company', 'N/A')}")
        print(f"    Name: {contact.get('first_name', '')} {contact.get('last_name', '')}")
        print(f"    Betreff: {subject[:50]}...")
        
        # Email senden
        if send_email(config, recipient, subject, text_body, html_body):
            sent_count += 1
            print(f"    ✅ Erfolgreich gesendet!")
        else:
            failed_count += 1
            print(f"    ❌ Versand fehlgeschlagen!")
        
        # Pause zwischen Emails (Anti-Spam)
        if i < len(contacts):
            wait_time = random.randint(5, 15)
            print(f"\n⏳ Warte {wait_time} Sekunden...")
            time.sleep(wait_time)
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"✅ Erfolgreich versendet: {sent_count}")
    print(f"❌ Fehlgeschlagen: {failed_count}")
    print(f"📧 Gesamt: {sent_count + failed_count}")
    
    if sent_count > 0:
        print("\n🎉 Emails wurden erfolgreich versendet!")
        print("\n📋 Nächste Schritte:")
        print("• Prüfe dein Email-Postfach für Antworten")
        print("• Follow-ups werden automatisch nach 2, 5, 7 Tagen gesendet")
        print("• Führe das Script täglich aus für kontinuierlichen Versand")
    
    print("\n💡 Tipp: Speichere dieses Script für zukünftige Kampagnen!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Abgebrochen vom Benutzer")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        print("\nPrüfe:")
        print("• email_config.json vorhanden und korrekt?")
        print("• email_templates.json vorhanden?")
        print("• email_contacts.csv vorhanden?")
        print("• App-Passwort korrekt eingetragen?")