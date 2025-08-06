const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const router = express.Router();

// Produkt-Konfiguration mit Stripe Preisen
const products = {
  'website-analyse': {
    name: 'Website-Analyse',
    price: 19700, // in Cents
    type: 'one_time',
    description: 'Detaillierte Analyse Ihrer Website mit Handlungsempfehlungen'
  },
  'website-quick': {
    name: 'Quick-Start Website',
    price: 49700,
    type: 'one_time',
    description: '3-5 Seiten, responsive Design, 3 Tage Lieferzeit'
  },
  'website-business': {
    name: 'Business Website',
    price: 99700,
    type: 'one_time',
    description: '7-10 Seiten, Premium Design, SEO-Optimierung'
  },
  'website-professional': {
    name: 'Professional Website',
    price: 179700,
    type: 'one_time',
    description: '10+ Seiten, Blog-System, E-Commerce ready'
  },
  'seo-starter': {
    name: 'SEO Starter',
    price: 29700,
    type: 'recurring',
    interval: 'month',
    description: '5 Keywords, monatlicher Report'
  },
  'seo-business': {
    name: 'SEO Business',
    price: 49700,
    type: 'recurring',
    interval: 'month',
    description: '15 Keywords, Backlink-Aufbau'
  },
  'seo-ads': {
    name: 'SEO + Ads Komplett',
    price: 79700,
    type: 'recurring',
    interval: 'month',
    description: '30 Keywords, Facebook/Instagram Ads'
  },
  'google-setup': {
    name: 'Google Basis-Setup',
    price: 29700,
    type: 'one_time',
    description: 'Google My Business, Analytics, Search Console'
  },
  'seo-setup': {
    name: 'SEO Komplett-Setup',
    price: 49700,
    type: 'one_time',
    description: 'Technical SEO Audit, Schema Markup'
  },
  'local-seo': {
    name: 'Local SEO Boost',
    price: 39700,
    type: 'one_time',
    description: 'Google My Business Optimierung'
  },
  'bundle': {
    name: 'Website + Analyse Bundle',
    price: 109700,
    type: 'one_time',
    description: 'Business Website + Website-Analyse im Bundle'
  },
  'mega-bundle': {
    name: 'MEGA-BUNDLE',
    price: 199700,
    type: 'one_time',
    description: 'Website + SEO-Setup + 3 Monate Betreuung'
  }
};

// Checkout Session erstellen
router.post('/create-checkout-session', async (req, res) => {
  try {
    const { productId, customerData } = req.body;
    const product = products[productId];

    if (!product) {
      return res.status(400).json({ error: 'Produkt nicht gefunden' });
    }

    // Session-Konfiguration
    const sessionConfig = {
      payment_method_types: ['card'],
      mode: product.type === 'recurring' ? 'subscription' : 'payment',
      success_url: `${process.env.SITE_URL || 'https://zukunfts-check.com'}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.SITE_URL || 'https://zukunfts-check.com'}/cancel`,
      customer_email: customerData.email,
      metadata: {
        productId: productId,
        customerName: `${customerData.firstName} ${customerData.lastName}`,
        company: customerData.company,
        phone: customerData.phone
      }
    };

    // Line Items konfigurieren
    if (product.type === 'recurring') {
      sessionConfig.line_items = [{
        price_data: {
          currency: 'eur',
          product_data: {
            name: product.name,
            description: product.description
          },
          recurring: {
            interval: product.interval || 'month'
          },
          unit_amount: product.price
        },
        quantity: 1
      }];
    } else {
      sessionConfig.line_items = [{
        price_data: {
          currency: 'eur',
          product_data: {
            name: product.name,
            description: product.description
          },
          unit_amount: product.price
        },
        quantity: 1
      }];
    }

    // Session erstellen
    const session = await stripe.checkout.sessions.create(sessionConfig);

    console.log('Checkout Session erstellt:', session.id);
    res.json({ url: session.url });

  } catch (error) {
    console.error('Stripe Error:', error);
    res.status(500).json({ 
      error: 'Fehler beim Erstellen der Checkout-Session',
      details: error.message 
    });
  }
});

// Webhook für erfolgreiche Zahlungen
router.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;

  try {
    event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET || 'your_webhook_secret'
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Event verarbeiten
  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;
      console.log('Payment successful for session:', session.id);
      // Hier können Sie E-Mail senden, Datenbank aktualisieren etc.
      break;
    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  res.json({ received: true });
});

module.exports = router;