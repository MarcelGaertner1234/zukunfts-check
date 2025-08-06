# 🚀 FutureCheck LinkedIn Automation Tool

Automatisiere deine LinkedIn-Outreach für FutureCheck mit personalisierten Nachrichten und intelligentem Follow-up System!

## ✨ Features

- 📊 **Lead-Management**: Import/Export von Kontakten via CSV
- 💬 **Personalisierte Nachrichten**: Branchen-spezifische Templates
- 🔄 **Automatisches Follow-up**: Nach 3, 7, 14 und 21 Tagen
- 📈 **A/B Testing**: Verschiedene Nachrichten-Varianten
- 🛡️ **LinkedIn-konform**: Respektiert Rate-Limits (max. 50/Tag)
- 📱 **Datenbank**: SQLite für Lead-Tracking und Statistiken

## 🚀 Quick Start

### 1. Installation

```bash
# Python 3.8+ erforderlich
cd futurecheck-mvp/linkedin-automation

# Keine externen Dependencies nötig!
# Alles läuft mit Python Standard-Bibliotheken
```

### 2. Erste Schritte

```bash
# Script starten
python linkedin_automation.py

# Menü-Optionen:
1. Leads aus CSV importieren
2. Nachrichten für heute generieren  
3. Statistiken anzeigen
4. Kampagne exportieren
5. Beenden
```

### 3. Workflow

#### Schritt 1: Leads sammeln
Exportiere Leads aus LinkedIn Sales Navigator oder nutze Tools wie:
- Apollo.io
- Hunter.io
- Phantombuster
- LinkedIn Helper

#### Schritt 2: CSV vorbereiten
Erstelle eine CSV mit folgenden Spalten:
```csv
first_name,last_name,position,company,industry,company_size,linkedin_url,email
Max,Mustermann,Geschäftsführer,Musterfirma GmbH,Handel,50-200,https://linkedin.com/in/max,
```

#### Schritt 3: Leads importieren
```bash
python linkedin_automation.py
# Wähle Option 1
# Gib Pfad zur CSV ein (oder Enter für 'leads.csv')
```

#### Schritt 4: Nachrichten generieren
```bash
# Option 2 wählen
# Anzahl festlegen (max. 50 pro Tag empfohlen)
# Nachrichten werden personalisiert generiert
```

#### Schritt 5: Kampagne exportieren
```bash
# Option 4 wählen
# Exportiert alle Nachrichten als CSV
# Diese kannst du dann verwenden in:
# - LinkedIn Sales Navigator
# - Automation Tools (Dux-Soup, Phantombuster)
# - Mail Merge
```

## 📁 Dateistruktur

```
linkedin-automation/
├── linkedin_automation.py   # Hauptscript
├── config.json              # Einstellungen (Limits, Branchen, etc.)
├── templates.json           # Nachrichten-Templates
├── leads.csv               # Beispiel-Leads (20 deutsche KMU)
├── database.db             # SQLite Datenbank (wird automatisch erstellt)
├── campaign_messages.csv   # Export-Datei (wird generiert)
└── README.md               # Diese Anleitung
```

## ⚙️ Konfiguration

### config.json anpassen:
```json
{
  "daily_limit": 50,           // Max. Nachrichten pro Tag
  "follow_up_days": [3,7,14],  // Follow-up Zeitpunkte
  "industries": [...],          // Ziel-Branchen
  "company_sizes": [...]        // Unternehmensgrößen
}
```

### Templates erweitern:
Bearbeite `templates.json` für neue Nachrichten-Varianten:
```json
{
  "initial": {
    "Handel": ["Template 1", "Template 2"],
    "Produktion": ["Template 1", "Template 2"]
  }
}
```

## 🎯 Best Practices

### LinkedIn Limits beachten:
- **Connection Requests**: Max. 100/Woche (empfohlen: 50)
- **Messages**: Max. 150/Tag (empfohlen: 30-50)
- **Profile Views**: Max. 1000/Tag
- **Arbeitszeiten**: Mo-Fr, 9-18 Uhr

### Nachrichten-Tipps:
1. **Personalisierung**: Nutze {first_name}, {company}, {position}
2. **Kurz & Knapp**: Max. 300 Zeichen für erste Nachricht
3. **Value First**: Zeige sofort den Nutzen
4. **Call-to-Action**: Klare nächste Schritte

### Follow-up Strategie:
- **1. Follow-up** (Tag 3): Kurze Erinnerung
- **2. Follow-up** (Tag 7): Case Study oder Erfolgsgeschichte
- **3. Follow-up** (Tag 14): Last Chance / Special Offer
- **4. Follow-up** (Tag 21): Kostenloser Mehrwert & Abschied

## 📊 Statistiken & Tracking

Das Tool trackt automatisch:
- Anzahl versendeter Nachrichten
- Response Rate
- Branchen-Verteilung
- Follow-up Performance

Statistiken abrufen:
```bash
python linkedin_automation.py
# Option 3: Statistiken anzeigen
```

## 🔗 Integration mit anderen Tools

### Export für LinkedIn Sales Navigator:
1. Campaign exportieren (Option 4)
2. CSV in Sales Navigator importieren
3. Nachrichten via InMail versenden

### Phantombuster Integration:
1. CSV exportieren
2. In Phantombuster "LinkedIn Message Sender" verwenden
3. Automatisch versenden lassen

### Dux-Soup Integration:
1. CSV mit LinkedIn URLs exportieren
2. In Dux-Soup importieren
3. Drip-Campaign starten

## ⚠️ Rechtliche Hinweise

- **DSGVO-konform**: Nur öffentlich verfügbare Daten nutzen
- **LinkedIn ToS**: Keine aggressive Automation
- **Opt-out**: Respektiere Ablehnungen sofort
- **B2B only**: Nur Geschäftskontakte anschreiben

## 🆘 Troubleshooting

### "Keine Leads gefunden"
→ CSV-Format prüfen, Spaltennnamen müssen exakt stimmen

### "Database locked"
→ Script neustarten, nur eine Instanz gleichzeitig

### "Keine passenden Templates"
→ templates.json prüfen, Branche muss übereinstimmen

## 📈 Erwartete Ergebnisse

Bei korrekter Nutzung:
- **Connection Accept Rate**: 20-30%
- **Response Rate**: 10-15%
- **Meeting Rate**: 3-5%
- **Conversion Rate**: 1-2%

Mit 500 Kontakten pro Woche:
- 100-150 neue Connections
- 50-75 Responses
- 15-25 Meetings
- 5-10 Kunden

## 🚀 Pro-Tipps

1. **Timing**: Dienstag-Donnerstag, 10-11 Uhr oder 14-15 Uhr
2. **Warming**: Neue Accounts langsam hochfahren (10→20→30→50)
3. **Variation**: Nutze verschiedene Templates (A/B Testing)
4. **Profile**: Optimiere dein LinkedIn-Profil vorher!
5. **Content**: Poste regelmäßig relevanten Content

## 💡 Nächste Schritte

1. Leads importieren ✓
2. Erste 50 Nachrichten generieren ✓
3. Via LinkedIn versenden
4. Responses tracken
5. Follow-ups planen
6. Meetings buchen!

---

**Viel Erfolg mit deiner LinkedIn-Kampagne!** 🚀

Bei Fragen: marcel@zukunfts-check.com