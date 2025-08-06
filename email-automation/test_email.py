#!/usr/bin/env python3
"""
Test-Script für Email-Versand
Testet ob deine SMTP-Konfiguration funktioniert
"""

import smtplib
import ssl
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def load_config():
    with open('email_config.json', 'r') as f:
        return json.load(f)

def send_test_email():
    print("📧 FutureCheck Email Test")
    print("=" * 50)
    
    config = load_config()
    smtp_config = config['smtp']
    
    if smtp_config['password'] == "HIER_APP_PASSWORT_EINFUEGEN":
        print("\n❌ FEHLER: Du musst erst dein App-Passwort eintragen!")
        print("\n📋 So geht's:")
        print("1. Gehe zu: https://myaccount.google.com/apppasswords")
        print("2. Erstelle ein App-Passwort für 'Mail'")
        print("3. Trage es in email_config.json ein")
        print("4. Starte dieses Script nochmal")
        return
    
    print(f"\n📮 Teste Email-Versand von: {smtp_config['email']}")
    
    test_email = input("\nAn welche Email soll der Test gehen? (Enter für deine eigene): ").strip()
    if not test_email:
        test_email = smtp_config['email']
    
    message = MIMEMultipart('alternative')
    message['From'] = f"{smtp_config['from_name']} <{smtp_config['email']}>"
    message['To'] = test_email
    message['Subject'] = "🎉 Test erfolgreich - FutureCheck Email Automation"
    
    text = f"""Hallo!

Dies ist eine Test-Email von deinem FutureCheck Email Automation System.

✅ Wenn du diese Email siehst, funktioniert alles!

Technische Details:
- Gesendet um: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
- Von: {smtp_config['email']}
- Server: {smtp_config['server']}
- Port: {smtp_config['port']}

Nächste Schritte:
1. Starte email_automation.py
2. Importiere Kontakte
3. Erstelle eine Kampagne
4. Versende echte Emails!

Viel Erfolg mit deiner Kampagne!

Beste Grüße
FutureCheck Automation System
"""
    
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h2 style="color: #007bff;">🎉 Test erfolgreich!</h2>
          
          <p>Dies ist eine Test-Email von deinem <strong>FutureCheck Email Automation System</strong>.</p>
          
          <div style="background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0;"><strong>✅ Wenn du diese Email siehst, funktioniert alles!</strong></p>
          </div>
          
          <h3>Technische Details:</h3>
          <ul>
            <li>Gesendet um: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</li>
            <li>Von: {smtp_config['email']}</li>
            <li>Server: {smtp_config['server']}</li>
            <li>Port: {smtp_config['port']}</li>
          </ul>
          
          <h3>Nächste Schritte:</h3>
          <ol>
            <li>Starte <code>email_automation.py</code></li>
            <li>Importiere Kontakte</li>
            <li>Erstelle eine Kampagne</li>
            <li>Versende echte Emails!</li>
          </ol>
          
          <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
            <p><strong>Viel Erfolg mit deiner Kampagne!</strong></p>
            <p>Beste Grüße<br>
            FutureCheck Automation System</p>
          </div>
        </div>
      </body>
    </html>
    """
    
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')
    
    message.attach(text_part)
    message.attach(html_part)
    
    try:
        print("\n⏳ Verbinde mit Gmail...")
        
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            print("📡 Verbindung hergestellt")
            
            if smtp_config['use_tls']:
                server.starttls(context=context)
                print("🔒 TLS aktiviert")
            
            print("🔑 Authentifiziere...")
            server.login(smtp_config['email'], smtp_config['password'])
            print("✅ Login erfolgreich!")
            
            print(f"📤 Sende Email an {test_email}...")
            server.send_message(message)
            
            print("\n" + "=" * 50)
            print("🎉 TEST ERFOLGREICH!")
            print("=" * 50)
            print(f"\n✅ Email wurde erfolgreich an {test_email} gesendet!")
            print("\n📋 Das bedeutet:")
            print("• Deine SMTP-Konfiguration funktioniert")
            print("• App-Passwort ist korrekt")
            print("• Du kannst jetzt die Automation starten")
            print("\n🚀 Starte jetzt: python email_automation.py")
            
    except smtplib.SMTPAuthenticationError:
        print("\n" + "=" * 50)
        print("❌ AUTHENTIFIZIERUNG FEHLGESCHLAGEN")
        print("=" * 50)
        print("\nMögliche Ursachen:")
        print("1. Falsches App-Passwort (prüfe Tippfehler)")
        print("2. 2FA nicht aktiviert (Voraussetzung für App-Passwörter)")
        print("3. Normales Passwort statt App-Passwort verwendet")
        print("\n📋 Lösung:")
        print("1. Gehe zu: https://myaccount.google.com/apppasswords")
        print("2. Erstelle ein NEUES App-Passwort")
        print("3. Kopiere es OHNE Leerzeichen")
        print("4. Trage es in email_config.json ein")
        
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP Fehler: {e}")
        print("\nPrüfe deine Internetverbindung und Firewall-Einstellungen")
        
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        print("\nBitte prüfe email_config.json auf Fehler")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("   FUTURECHECK EMAIL TEST")
    print("=" * 50)
    
    print("\n⚠️  SICHERHEITSCHECK:")
    print("• Hast du dein Gmail-Passwort geändert? (Nach dem Leak)")
    print("• Hast du 2FA aktiviert?")
    print("• Hast du ein App-Passwort erstellt?")
    
    proceed = input("\nAlle Sicherheitsmaßnahmen erledigt? (j/n): ")
    
    if proceed.lower() != 'j':
        print("\n❌ Bitte erst die Sicherheitsmaßnahmen durchführen!")
        print("Lies: SICHERHEIT_WICHTIG.md")
    else:
        send_test_email()