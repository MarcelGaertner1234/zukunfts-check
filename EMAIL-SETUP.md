# 📧 E-Mail Setup - FutureCheck Pro

## 🚀 Quick Setup

### 1. Environment Variables einrichten
```bash
# Kopiere die Beispiel-Datei
cp .env.example .env

# Bearbeite die .env Datei mit deinen Daten
```

### 2. Gmail App-Password erstellen
1. Gehe zu https://myaccount.google.com/security
2. Aktiviere "2-Step Verification" falls noch nicht aktiv
3. Gehe zu "App passwords" (unter Security)
4. Wähle "Mail" und "Other (Custom name)"
5. Gib "FutureCheck Pro" als Name ein
6. Kopiere das generierte 16-stellige Passwort
7. Füge es in die `.env` Datei unter `EMAIL_PASS` ein

### 3. .env Datei konfigurieren
```env
# Deine echten Stripe Keys einfügen
STRIPE_SECRET_KEY=sk_test_DEINE_ECHTEN_KEYS
STRIPE_PUBLISHABLE_KEY=pk_test_DEINE_ECHTEN_KEYS
STRIPE_WEBHOOK_SECRET=whsec_DEINE_ECHTEN_KEYS

# Gmail Konfiguration
EMAIL_USER=gaertner-marcel@web.de
EMAIL_PASS=abcd efgh ijkl mnop  # Das 16-stellige App Password

# Server
PORT=3001
NODE_ENV=development
DOMAIN=http://localhost:3001
```

## 🔧 Alternative E-Mail Provider

### Web.de / GMX Setup
```env
EMAIL_HOST=smtp.web.de
EMAIL_PORT=587
EMAIL_USER=gaertner-marcel@web.de
EMAIL_PASS=dein_web_de_passwort
```

### Office365 / Outlook Setup
```env
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USER=deine@firma.com
EMAIL_PASS=dein_outlook_passwort
```

## 📨 Wie das E-Mail System funktioniert

### Workflow:
1. **Kunde füllt Formular aus** → `kundendaten.html`
2. **Daten werden per E-Mail gesendet** → Du bekommst sofort eine E-Mail
3. **Kunde wird zu Stripe weitergeleitet** → Bezahlung
4. **Stripe sendet Webhook** → Du bekommst zweite E-Mail mit Zahlungsbestätigung

### Du bekommst 2 E-Mails:

#### 📋 E-Mail 1: "Neue Kundenanfrage"
```
🎉 NEUE KUNDENANFRAGE - FutureCheck Pro

📦 PRODUKT: Website-Analyse
💰 PREIS: 197€

👤 KUNDENDATEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: Max Mustermann
E-Mail: max@firma.de
Telefon: +49 123 456789
Firma: Mustermann GmbH
...
```

#### 💰 E-Mail 2: "Zahlung erhalten"
```
💳 ZAHLUNG EINGEGANGEN - FutureCheck Pro

💰 Betrag: 197€
📦 Produkt: Website-Analyse
👤 Kunde: max@firma.de
⏰ Bezahlt: 06.08.2025, 19:45
```

## 🧪 Testing

### Testen ohne echte E-Mails:
1. Kommentiere die `transporter.sendMail()` Zeilen aus
2. Verwende stattdessen `console.log()` 
3. Alle E-Mails werden in der Konsole angezeigt

### Test-Workflow:
1. `npm run dev` starten
2. http://localhost:3001 öffnen
3. "Website-Analyse" auswählen
4. Formular ausfüllen
5. "Weiter zur Bezahlung" klicken
6. E-Mail sollte in deinem Postfach ankommen
7. Stripe Test-Karte verwenden: `4242 4242 4242 4242`

## 🐛 Troubleshooting

### "Authentication failed" Fehler:
- ✅ 2-Factor Authentication aktiviert?
- ✅ App Password (nicht normales Passwort) verwendet?
- ✅ Correct Email/Password in .env?

### "Connection timeout" Fehler:
- ✅ Internet-Verbindung OK?
- ✅ Firewall/Antivirus blockiert Port 587?

### E-Mails kommen nicht an:
- ✅ Spam-Ordner prüfen
- ✅ Server läuft: `npm run dev`
- ✅ Browser-Konsole auf Fehler prüfen

## 🔒 Sicherheit

- ✅ Niemals `.env` Datei committen
- ✅ App Passwords verwenden (nicht Haupt-Passwort)
- ✅ `.env` ist bereits in `.gitignore`

## 📞 Support

Bei Problemen:
- Email: gaertner-marcel@web.de  
- Tel: +41 76 801 53 30