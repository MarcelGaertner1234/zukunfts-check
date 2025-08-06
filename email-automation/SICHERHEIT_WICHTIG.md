# 🚨 WICHTIGE SICHERHEITSHINWEISE 🚨

## ⚠️ SOFORT-MAßNAHMEN:

### 1. PASSWORT ÄNDERN (JETZT!)
Da du dein Passwort öffentlich geteilt hast:
1. Gehe zu: https://myaccount.google.com/security
2. Ändere SOFORT dein Gmail-Passwort
3. Prüfe die letzten Aktivitäten auf verdächtige Zugriffe

### 2. 2-FAKTOR-AUTHENTIFIZIERUNG AKTIVIEREN
1. https://myaccount.google.com/signinoptions/two-step-verification
2. Aktiviere 2FA mit deinem Smartphone
3. Speichere die Backup-Codes sicher

### 3. APP-PASSWORT ERSTELLEN (für Email-Automation)
1. Gehe zu: https://myaccount.google.com/apppasswords
2. Wähle "Mail" aus dem Dropdown
3. Klicke "Generieren"
4. Kopiere das 16-stellige Passwort (Format: xxxx-xxxx-xxxx-xxxx)

## ✅ SO RICHTEST DU DIE EMAIL-AUTOMATION EIN:

### Schritt 1: App-Passwort in Config eintragen
```bash
cd futurecheck-mvp/email-automation
```

Bearbeite `email_config.json`:
- Ersetze "HIER_APP_PASSWORT_EINFUEGEN" mit deinem App-Passwort
- NICHT dein normales Gmail-Passwort verwenden!

### Schritt 2: Test-Email versenden
```bash
python email_automation.py
# Wähle Option 3: Emails versenden
# Teste mit 1 Email an dich selbst
```

## 🔐 SICHERHEITS-REGELN:

### NIEMALS:
- ❌ Dein echtes Passwort in Dateien speichern
- ❌ Passwörter öffentlich teilen (auch nicht mit mir!)
- ❌ Passwörter in Git committen
- ❌ 2FA deaktivieren

### IMMER:
- ✅ App-Passwörter für Automatisierung nutzen
- ✅ Verschiedene Passwörter für verschiedene Dienste
- ✅ Passwort-Manager verwenden (z.B. Bitwarden, 1Password)
- ✅ 2FA überall aktivieren

## 📧 GMAIL APP-PASSWORT ANLEITUNG:

### Warum App-Passwort?
- Sicherer als Haupt-Passwort
- Kann jederzeit widerrufen werden
- Funktioniert mit 2FA
- Speziell für Apps/Scripts

### So erstellst du es:
1. **Gmail öffnen** → Einstellungen → Sicherheit
2. **2FA muss aktiv sein** (Voraussetzung!)
3. **App-Passwörter** → "Mail" auswählen
4. **Generieren** klicken
5. **16-stelliges Passwort** kopieren
6. In `email_config.json` einfügen

### Beispiel email_config.json:
```json
{
  "smtp": {
    "email": "gaertnerstoreangel@gmail.com",
    "password": "abcd-efgh-ijkl-mnop"  // Dein App-Passwort hier
  }
}
```

## 🚀 NACH DER EINRICHTUNG:

### Email-Automation starten:
```bash
cd futurecheck-mvp/email-automation
python email_automation.py

# Menü:
1. Kontakte importieren (email_contacts.csv)
2. Neue Kampagne erstellen
3. Emails versenden (startet Versand)
4. Statistiken anzeigen
```

### Erste Kampagne:
1. Option 1: Kontakte importieren
2. Option 2: Kampagne "Test" erstellen
3. Option 3: 5 Test-Emails versenden
4. Prüfe ob Emails ankommen

## ⚠️ WEITERE SICHERHEITSTIPPS:

1. **Backup deiner Daten**:
   - Exportiere Kontakte regelmäßig
   - Sichere deine Datenbank

2. **Monitoring**:
   - Prüfe Gmail-Aktivitäten täglich
   - Achte auf Bounce-Mails
   - Überwache Spam-Reports

3. **Rate Limits beachten**:
   - Max 500 Emails/Tag (Gmail)
   - Max 50 pro Stunde empfohlen
   - Warmup bei neuem Account

## 🆘 HILFE BEI PROBLEMEN:

### "Authentication failed"
→ App-Passwort prüfen (keine Leerzeichen!)
→ 2FA muss aktiv sein
→ "Weniger sichere Apps" NICHT aktivieren

### "Quota exceeded"
→ Gmail Limit erreicht (500/Tag)
→ 24h warten
→ Oder anderen Account nutzen

### Account gesperrt?
→ https://accounts.google.com/DisplayUnlockCaptcha
→ Entsperren und App-Passwort neu erstellen

---

**WICHTIG**: Lösche diese Datei NICHT! Sie enthält wichtige Sicherheitshinweise.

**Bei Fragen**: Erstelle ein neues App-Passwort und versuche es nochmal. 
Teile NIEMALS dein echtes Passwort!

Viel Erfolg und bleib sicher! 🔒