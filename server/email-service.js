let nodemailer;
try {
    nodemailer = require('nodemailer');
} catch (error) {
    console.warn('Nodemailer not available - email functionality disabled');
    nodemailer = {
        createTransporter: () => ({
            sendMail: async () => ({ messageId: 'mock-id', success: false })
        })
    };
}

// E-Mail Transporter Setup
const transporter = nodemailer.createTransporter({
    host: 'smtp.gmail.com',
    port: 587,
    secure: false,
    auth: {
        user: process.env.EMAIL_USER, // deine Gmail Adresse
        pass: process.env.EMAIL_PASS  // Gmail App-Password
    }
});

// Alternative: Verwende deinen bestehenden E-Mail Provider
// const transporter = nodemailer.createTransporter({
//     host: 'mail.your-provider.com',
//     port: 587,
//     secure: false,
//     auth: {
//         user: process.env.EMAIL_USER,
//         pass: process.env.EMAIL_PASS
//     }
// });

// Kundendaten E-Mail an dich senden
async function sendCustomerDataEmail(customerData) {
    try {
        const productInfo = {
            'website-analyse': { name: 'Website-Analyse', price: '197€' },
            'website-quick': { name: 'Quick-Start Website', price: '497€' },
            'website-business': { name: 'Business Website', price: '997€' },
            'website-professional': { name: 'Professional Website', price: '1.797€' },
            'seo-starter': { name: 'SEO Starter', price: '297€/Monat' },
            'seo-business': { name: 'SEO Business', price: '497€/Monat' },
            'seo-ads': { name: 'SEO + Ads Komplett', price: '797€/Monat' },
            'google-setup': { name: 'Google Basis-Setup', price: '297€' },
            'seo-setup': { name: 'SEO Komplett-Setup', price: '497€' },
            'bundle': { name: 'Website + Analyse Bundle', price: '1.097€' },
            'mega-bundle': { name: 'MEGA-BUNDLE', price: '1.997€' }
        };

        const product = productInfo[customerData.product] || { name: 'Unbekannt', price: '0€' };

        const emailContent = `
🎉 NEUE KUNDENANFRAGE - FutureCheck Pro

📦 PRODUKT: ${product.name}
💰 PREIS: ${product.price}

👤 KUNDENDATEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: ${customerData.firstName} ${customerData.lastName}
E-Mail: ${customerData.email}
Telefon: ${customerData.phone}
Firma: ${customerData.company}

📍 ADRESSE:
${customerData.street || 'Nicht angegeben'}
${customerData.zip || ''} ${customerData.city || ''}
${customerData.country || 'DE'}

${customerData.currentWebsite ? `🌐 AKTUELLE WEBSITE: ${customerData.currentWebsite}` : ''}
${customerData.websiteUrl ? `🌐 WEBSITE-URL: ${customerData.websiteUrl}` : ''}
${customerData.industry ? `🏢 BRANCHE: ${customerData.industry}` : ''}
${customerData.mainKeywords ? `🔍 KEYWORDS: ${customerData.mainKeywords}` : ''}
${customerData.competitors ? `🎯 KONKURRENTEN: ${customerData.competitors}` : ''}
${customerData.goals ? `📋 ZIELE: ${customerData.goals}` : ''}
${customerData.notes ? `💭 ANMERKUNGEN: ${customerData.notes}` : ''}

Newsletter: ${customerData.newsletter ? '✅ Ja' : '❌ Nein'}

⏰ Eingegangen: ${new Date().toLocaleString('de-DE')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👆 Kunde wird jetzt zur Stripe-Zahlung weitergeleitet.
Du bekommst gleich eine separate E-Mail wenn die Zahlung eingegangen ist.
        `;

        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: 'gaertner-marcel@web.de', // deine E-Mail
            subject: `🔥 Neue Bestellung: ${product.name} - ${customerData.firstName} ${customerData.lastName}`,
            text: emailContent
        };

        const result = await transporter.sendMail(mailOptions);
        console.log('Customer data email sent:', result.messageId);
        return { success: true, messageId: result.messageId };

    } catch (error) {
        console.error('Error sending customer data email:', error);
        return { success: false, error: error.message };
    }
}

// Zahlungsbestätigung E-Mail
async function sendPaymentConfirmationEmail(paymentData) {
    try {
        const emailContent = `
💳 ZAHLUNG EINGEGANGEN - FutureCheck Pro

💰 Betrag: ${paymentData.amount}€
📦 Produkt: ${paymentData.product || 'Nicht spezifiziert'}
🔗 Stripe ID: ${paymentData.paymentId}
👤 Kunde: ${paymentData.customerEmail || 'Nicht verfügbar'}

⏰ Bezahlt: ${new Date().toLocaleString('de-DE')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Nächste Schritte:
1. Kundendaten-E-Mail suchen (gleicher Zeitraum)
2. Projekt starten
3. Kunden kontaktieren
        `;

        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: 'gaertner-marcel@web.de',
            subject: `💰 Zahlung erhalten: ${paymentData.amount}€ - ${paymentData.customerEmail}`,
            text: emailContent
        };

        const result = await transporter.sendMail(mailOptions);
        console.log('Payment confirmation email sent:', result.messageId);
        return { success: true, messageId: result.messageId };

    } catch (error) {
        console.error('Error sending payment confirmation email:', error);
        return { success: false, error: error.message };
    }
}

module.exports = {
    sendCustomerDataEmail,
    sendPaymentConfirmationEmail
};