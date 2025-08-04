# FutureCheck - Digital Maturity Assessment

**Live:** [zukunfts-check.com](https://zukunfts-check.com)  
**Repository:** [GitHub](https://github.com/MarcelGaertner1234/zukunfts-check)

## 🎯 Projekt-Übersicht

Digitale Reifegradanalyse für KMU - Von ahnungslos zu zukunftsfit in 24 Stunden.

### Kernfunktionen
- Digital Maturity Score (0-100)
- Konkurrenzanalyse
- 3 priorisierte Handlungsempfehlungen
- ROI-Berechnungen
- 30-seitiger PDF-Report

## ✅ Status

**LIVE & FUNKTIONSFÄHIG** 
- Formspree Integration ✅ (ID: movlkqpp)
- Stripe Payment Links ✅ (Live-Modus)
- Netlify Auto-Deploy ✅
- Mobile Optimized ✅
- DSGVO-konform ✅

## 🛠️ Konfiguration

Alle Einstellungen findest du in `config.js`:

```javascript
// Formspree (E-Mail) - SUPER EINFACH!
formspree: {
    formId: 'YOUR_FORM_ID' // Von formspree.io
}

// Stripe Einstellungen
stripe: {
    paymentLink: 'YOUR_PAYMENT_LINK'
}

// Features aktivieren
features: {
    demoMode: false,          // Auf false für Live
    formspreeEnabled: true,   // Formspree aktivieren
    stripeEnabled: true       // Stripe aktivieren
}
```

**WICHTIG:** Du musst auch die Form Action in `checkout.html` Zeile 245 anpassen:
```html
action="https://formspree.io/f/YOUR_FORM_ID"
```

## 📁 Dateistruktur

```
futurecheck-mvp/
├── index.html           # Landing Page
├── checkout.html        # Checkout-Formular  
├── danke.html          # Bestätigungsseite
├── impressum.html      # Impressum
├── datenschutz.html    # Datenschutz
├── styles.css          # Styling
├── config.js           # Konfiguration
└── marketing/          # Marketing-Materialien
    ├── marketing-strategy.md
    ├── linkedin-templates.md
    ├── cold-email-templates.md
    └── action-plan-week1.md
```

## 🚀 Deploy auf Netlify

1. **GitHub Repository erstellen**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```

2. **Netlify Deploy**
   - Gehe zu [app.netlify.com](https://app.netlify.com)
   - "New site from Git"
   - GitHub verbinden
   - Repository auswählen
   - Deploy!

3. **Custom Domain**
   - In Netlify: Domain Settings
   - Add custom domain
   - DNS einrichten

## 💰 Geschäftsmodell

- **Early Bird:** 197€ (erste 20 Kunden)
- **Regulär:** 497€
- **Lieferung:** 24 Stunden
- **Leistung:** 30-seitiger PDF-Report + 30 Min Beratung

## 🎯 Zielgruppe

- **KMU** (10-200 Mitarbeiter)
- **Branchen:** Handel, Produktion, Handwerk, Dienstleistung
- **Problem:** Digitalisierungslücke zur Konkurrenz

## 📈 Marketing

Komplette Marketing-Strategie und Templates im `/marketing/` Ordner:
- 500+ LinkedIn Templates
- Cold Email Sequenzen
- Aktionsplan Woche 1
- Conversion-optimierte Nachrichten

## 🆘 Support

Bei Fragen:
- Formspree Docs: https://help.formspree.io/
- Stripe Docs: https://stripe.com/docs
- Netlify Docs: https://docs.netlify.com/

---

**© 2025 FutureCheck** - Von ahnungslos zu zukunftsfit in 24 Stunden 🚀