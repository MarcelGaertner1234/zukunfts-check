# 📧 FutureCheck Email Automation System

Professionelles Email-Marketing-System mit 7-stufiger Follow-up Sequenz für maximale Conversion!

## 🚀 Features

- 📊 **7-Email Sequenz**: Automatisches Follow-up über 30 Tage
- 🎯 **Personalisierung**: Dynamische Platzhalter für jeden Kontakt
- 📈 **Tracking**: Opens, Clicks, Replies automatisch tracken
- 🔄 **A/B Testing**: Verschiedene Betreffzeilen testen
- 🛡️ **DSGVO-konform**: Unsubscribe & Datenschutz integriert
- 📱 **Responsive HTML**: Perfekt auf allen Geräten
- ⏰ **Smart Timing**: Nur zu Geschäftszeiten versenden
- 💾 **SQLite Datenbank**: Komplettes CRM integriert

## ⚡ Quick Start

### 1. Installation

```bash
cd futurecheck-mvp/email-automation

# Python 3.8+ erforderlich
# Keine externen Dependencies nötig!
```

### 2. SMTP einrichten

Bearbeite `email_config.json`:
```json
{
  "smtp": {
    "email": "deine-email@gmail.com",
    "password": "dein-app-passwort"
  }
}
```

**Für Gmail:**
1. Gehe zu: https://myaccount.google.com/apppasswords
2. Erstelle App-Passwort für "Mail"
3. Nutze dieses Passwort (NICHT dein normales Passwort!)

**Für andere Provider:**
- **Outlook**: smtp.office365.com (Port 587)
- **Yahoo**: smtp.mail.yahoo.com (Port 587)
- **ProtonMail**: smtp.protonmail.com (Port 587)

### 3. Script starten

```bash
python email_automation.py

# Menü:
1. 📥 Kontakte importieren
2. 🚀 Kampagne starten
3. 📤 Emails versenden
4. 📊 Statistiken
5. 💾 Export
6. ⚙️  Setup
7. 🚪 Exit
```

## 📋 Workflow

### Schritt 1: Kontakte sammeln
Quellen für B2B Email-Adressen:
- **Hunter.io**: Domain-basierte Email-Suche
- **Apollo.io**: B2B Kontakt-Datenbank
- **Clearbit**: Company & Contact API
- **LinkedIn Sales Navigator**: Export via Tools
- **Eigene Website**: Formular-Submissions

### Schritt 2: CSV vorbereiten
Format für `email_contacts.csv`:
```csv
email,first_name,last_name,company,position,industry,company_size
max@firma.de,Max,Muster,Firma GmbH,CEO,Handel,50-200
```

### Schritt 3: Kampagne erstellen
```bash
python email_automation.py
# Option 2: Neue Kampagne
# Name eingeben
# Kontakte werden automatisch hinzugefügt
```

### Schritt 4: Emails versenden
```bash
# Option 3: Queue abarbeiten
# System versendet automatisch:
# - Max 20/Stunde (konfigurierbar)
# - Max 100/Tag (Gmail Limit)
# - Nur Mo-Fr, 9-17 Uhr
```

## 📧 Email-Sequenz (7 Emails über 30 Tage)

### Tag 0: Initial Contact
**Betreff**: "🚀 {company} - Digitaler Reifegrad in 24h erfahren"
- Problemstellung
- Lösung präsentieren
- Early-Bird Angebot

### Tag 2: Follow-up 1
**Betreff**: "Re: {company} - Kurze Nachfrage (2 Min Video)"
- Video-Demo
- Social Proof
- Termin-Link

### Tag 5: Value Email
**Betreff**: "💡 {first_name}, kostenlose Checkliste für {industry}"
- Kostenloses Whitepaper
- Mehrwert ohne Verkauf
- Trust aufbauen

### Tag 7: Case Study
**Betreff**: "📊 Erfolgsgeschichte: 150 MA Unternehmen aus {industry}"
- Konkrete Zahlen
- ROI demonstrieren
- Glaubwürdigkeit

### Tag 14: Urgency
**Betreff**: "⏰ {first_name}, nur noch 3 Early-Bird Plätze"
- Knappheit
- Preisunterschied
- Direkt-Link

### Tag 21: Last Chance
**Betreff**: "🎁 {first_name}, mein letztes Angebot für {company}"
- Exklusiv-Deal
- Bonus-Leistungen
- 48h Frist

### Tag 30: Break-up
**Betreff**: "👋 {first_name}, alles Gute für {company}"
- Freundlicher Abschied
- Kostenlose Tipps
- Tür offen lassen

## 📊 Tracking & Analytics

Das System trackt automatisch:
- **Opens**: Tracking-Pixel in HTML
- **Clicks**: UTM-Parameter auf Links
- **Replies**: Manual tracking
- **Unsubscribes**: Automatisch

### Statistiken abrufen:
```bash
python email_automation.py
# Option 4: Kampagnen-Statistiken

Beispiel-Output:
📊 Kampagne: Q1 2025 Launch
Kontakte: 500
Versendet: 350
Öffnungsrate: 42.3%
Klickrate: 12.7%
Antwortrate: 4.2%
```

## ⚙️ Konfiguration

### email_config.json anpassen:

```json
{
  "campaign": {
    "daily_limit": 100,        // Max Emails/Tag
    "hourly_limit": 20,        // Max Emails/Stunde
    "sequence_delays": [0,2,5,7,14,21,30], // Tage
    "working_hours": {
      "start": "09:00",
      "end": "17:00"
    }
  },
  "warmup": {
    "enabled": true,           // Email-Account aufwärmen
    "start_volume": 10,        // Start mit 10/Tag
    "daily_increase": 10       // +10 jeden Tag
  }
}
```

## 🎯 Best Practices

### Email Deliverability:
1. **Warmup**: Neue Accounts langsam hochfahren
2. **SPF/DKIM**: DNS-Records einrichten
3. **Sender Score**: Reputation überwachen
4. **Bounce Rate**: Unter 2% halten
5. **Spam Words**: Vermeiden ("Gratis", "€€€", "!!!")

### Timing:
- **Beste Tage**: Dienstag - Donnerstag
- **Beste Zeit**: 10-11 Uhr, 14-15 Uhr
- **Vermeide**: Montag morgen, Freitag nachmittag

### Content:
- **Betreffzeile**: Max. 60 Zeichen
- **Preview Text**: Erste 90 Zeichen wichtig
- **Personalisierung**: Name, Firma, Branche
- **CTA**: Nur 1 klarer Call-to-Action
- **Mobile**: 65% lesen auf Handy

## 🔗 Integration mit anderen Tools

### CRM Integration:
```python
# Export für HubSpot/Pipedrive
python email_automation.py
# Option 5: Daten exportieren
# CSV importieren in CRM
```

### Webhook für Zapier:
```json
// In email_config.json:
"notifications": {
  "webhook_url": "https://hooks.zapier.com/..."
}
```

### Mailchimp/SendinBlue Migration:
1. Kontakte exportieren als CSV
2. Templates kopieren
3. In Tool importieren

## 📈 Erwartete Ergebnisse

Bei korrekter Nutzung:
- **Open Rate**: 30-40%
- **Click Rate**: 8-12%
- **Reply Rate**: 3-5%
- **Conversion**: 1-2%

Mit 1000 Emails/Woche:
- 350 Opens
- 100 Clicks
- 40 Replies
- 10-20 Meetings
- 5-10 Kunden

## 🛡️ Rechtliche Hinweise

### DSGVO Compliance:
- ✅ Geschäftliche Emails nur an Firmen-Adressen
- ✅ Berechtigtes Interesse (B2B)
- ✅ Unsubscribe-Link in jeder Email
- ✅ Datenschutzerklärung verlinkt
- ✅ Keine Weitergabe an Dritte

### CAN-SPAM Act:
- ✅ Kein irreführender Betreff
- ✅ Absender klar erkennbar
- ✅ Physische Adresse angegeben
- ✅ Opt-out innerhalb 10 Tagen

## 🚨 Troubleshooting

### "SMTP Authentication failed"
→ App-Passwort verwenden, nicht normales Passwort

### "Connection timed out"
→ Firewall/Antivirus prüfen, Port 587 freigeben

### "Daily limit reached"
→ Gmail: Max 500/Tag, Outlook: 300/Tag

### "High bounce rate"
→ Email-Validierung nutzen (NeverBounce, ZeroBounce)

### "Marked as spam"
→ SPF/DKIM einrichten, Spam-Words vermeiden

## 💡 Pro-Tipps

1. **Double Opt-in**: Bei eigener Liste immer bestätigen lassen
2. **Segmentierung**: Nach Branche/Größe trennen
3. **Re-Engagement**: Inaktive nach 60 Tagen entfernen
4. **Testing**: Immer an eigene Adresse testen
5. **Backup**: Datenbank regelmäßig sichern

## 📚 Weiterführende Ressourcen

- **Email Deliverability**: https://www.mail-tester.com
- **SPF/DKIM Setup**: https://mxtoolbox.com
- **GDPR for Email**: https://gdpr.eu/email-encryption/
- **Cold Email Templates**: https://lemlist.com/cold-email-templates

## 🎯 Nächste Schritte

1. ✅ SMTP einrichten
2. ✅ 100 Kontakte importieren
3. ✅ Erste Kampagne starten
4. ✅ 10 Test-Emails versenden
5. ✅ Statistiken prüfen
6. ✅ Skalieren auf 100/Tag

---

**Viel Erfolg mit deiner Email-Kampagne!** 📧🚀

Bei Fragen: marcel@zukunfts-check.com