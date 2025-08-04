# FutureCheck MVP - Landing Page

## 🚀 Quick Start Guide

Diese ultra-simple Landing Page ist bereit für den Launch! Hier ist alles, was du wissen musst:

## ✅ Was ist fertig?

- **Landing Page** mit klarem Angebot (197€ Early Bird)
- **Checkout-Flow** mit Formular
- **EmailJS Integration** (E-Mail-Benachrichtigungen)
- **Stripe Payment Links** (Zahlungsabwicklung)
- **Rechtliche Seiten** (Impressum, Datenschutz)
- **SEO-Optimierung** (Meta Tags)
- **Mobile Responsive** Design

## 📋 Launch-Checkliste

### 1. Formspree einrichten (NUR 2 MINUTEN!)
- [ ] Gehe zu [formspree.io](https://formspree.io)
- [ ] Gib deine E-Mail ein (kein Account nötig!)
- [ ] Kopiere die Form ID
- [ ] Füge sie in `checkout.html` Zeile 245 ein
- [ ] Anleitung: Öffne `formspree-setup.html`

### 2. Stripe einrichten (15 Min)
- [ ] Account bei [Stripe.com](https://stripe.com) erstellen
- [ ] Produkt anlegen (197€)
- [ ] Payment Link generieren
- [ ] Link in `config.js` eintragen
- [ ] Anleitung: Öffne `stripe-setup.html`

### 3. Rechtliches anpassen
- [ ] `impressum.html` - Alle [PLATZHALTER] ersetzen
- [ ] `datenschutz.html` - Alle [PLATZHALTER] ersetzen
- [ ] Optional: AGB erstellen

### 4. Domain & Hosting
- [ ] Domain registrieren (z.B. digitaler-check.de)
- [ ] Bei Netlify deployen (kostenlos)
- [ ] Domain verbinden
- [ ] SSL aktivieren (automatisch)

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
├── impressum.html      # Impressum (anpassen!)
├── datenschutz.html    # Datenschutz (anpassen!)
├── styles.css          # Styling
├── config.js           # Konfiguration
├── formspree-setup.html # Formspree Anleitung (2 Min!)
└── stripe-setup.html    # Stripe Anleitung
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

## 💰 Der Prozess

1. **Kunde bestellt** → Zahlt 197€ via Stripe
2. **Du bekommst E-Mail** → Mit allen Kundendaten
3. **Du analysierst** (2-3 Stunden):
   - Website mit Tools checken
   - Konkurrenz anschauen
   - Report in Canva erstellen
4. **PDF versenden** → Per E-Mail an Kunden
5. **Optional: Zoom Call** → 30 Min Beratung

## 📊 Erste Kunden gewinnen

### LinkedIn-Strategie
```
"Hi [Name], 
ich helfe KMUs dabei, ihren digitalen Reifegrad zu verstehen.
Für nur 197€ (statt üblicher 10.000€ Beraterkosten) analysiere 
ich Ihre Website und liefere konkrete Handlungsempfehlungen.
Interesse an einem kostenlosen 10-Min-Gespräch?"
```

### Zielgruppen
- Geschäftsführer von KMU (50-500 MA)
- Branchen: Handel, Produktion, Dienstleistung
- Problem: Wissen nicht, wo sie digital stehen

## ⚡ Nächste Schritte

### Sofort (Nur 30 Minuten!)
1. Formspree einrichten (2 Min)
2. Stripe einrichten (15 Min)
3. Rechtliches anpassen (10 Min)
4. Auf Netlify deployen (3 Min)

### Diese Woche (Tag 3-7)
1. 10 LinkedIn-Nachrichten senden
2. 3 Test-Kunden gewinnen
3. Erste Analysen durchführen
4. Feedback sammeln

### Nach 10 Kunden
- Automatisierung planen
- Prozess optimieren
- Preis erhöhen (497€)

## 🆘 Support

Bei Fragen:
- Formspree Docs: https://help.formspree.io/
- Stripe Docs: https://stripe.com/docs
- Netlify Docs: https://docs.netlify.com/

## 📝 Notizen

- **KISS Prinzip**: Keep It Simple, Stupid!
- **Keine Perfektion**: Launch > Perfection
- **Lernen**: Jeder Kunde = Feedback
- **Skalieren**: Erst manuell, dann automatisieren

---

**Ready to Launch?** 🚀 Die ersten 197€ sind nur einen Klick entfernt!