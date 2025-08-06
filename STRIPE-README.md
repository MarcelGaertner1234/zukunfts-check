# Stripe Integration - FutureCheck Pro

## 🚀 Quick Start

### 1. Installation
```bash
# Install dependencies
npm install

# Or run the setup script
./setup-stripe.sh
```

### 2. Stripe Account Setup
1. Create a Stripe account at https://stripe.com
2. Get your API keys from https://dashboard.stripe.com/apikeys
3. Copy `.env.example` to `.env` and add your keys:
```env
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
```

### 3. Update Frontend
Edit `checkout-stripe.html` line 509 and add your publishable key:
```javascript
const stripe = Stripe('pk_test_YOUR_PUBLISHABLE_KEY');
```

### 4. Start the Server
```bash
# Development
npm run dev

# Production
npm start
```

## 💳 Available Products

| Product | ID | Price |
|---------|-----|-------|
| Website-Analyse | `analysis` | 197€ |
| Website Quick-Start | `website-quick` | 497€ |
| Website Business | `website-business` | 997€ |
| Website Professional | `website-professional` | 1797€ |
| SEO Setup | `seo-setup` | 297€ |
| SEO Betreuung | `seo-monthly` | 297€/Monat |
| MEGA-BUNDLE | `bundle` | 1997€ |

## 📁 File Structure

```
futurecheck-mvp/
├── checkout-stripe.html     # Stripe checkout page
├── server/
│   ├── index.js            # Express server
│   └── stripe-api.js       # Stripe API endpoints
├── .env                    # Environment variables (create from .env.example)
├── package.json            # Dependencies
└── index-multi.html        # Main landing page
```

## 🔗 API Endpoints

### Create Payment Intent
```
POST /api/create-payment-intent
```
```json
{
  "amount": 19700, // in cents
  "customer": {
    "email": "customer@example.com",
    "name": "John Doe",
    "metadata": {
      "product": "Website-Analyse"
    }
  }
}
```

### Create Checkout Session
```
POST /api/create-checkout-session
```
```json
{
  "productId": "analysis",
  "customerEmail": "customer@example.com"
}
```

### Webhook Handler
```
POST /api/webhook
```
Handles Stripe webhook events (payment success, etc.)

## 🧪 Testing

### Test Cards
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- 3D Secure: `4000 0025 0000 3155`

### Test Flow
1. Open http://localhost:3001
2. Select a product
3. Click "Jetzt starten"
4. Fill in the checkout form
5. Use test card `4242 4242 4242 4242`
6. Any future date for expiry
7. Any 3 digits for CVC
8. Any 5 digits for postal code

## 🔒 Security

- ✅ PCI DSS compliant (Stripe handles card data)
- ✅ SSL/TLS required in production
- ✅ Webhook signature verification
- ✅ CORS configured
- ✅ Helmet.js for security headers

## 📱 Webhook Setup (Production)

### Local Testing
```bash
stripe listen --forward-to localhost:3001/api/webhook
```

### Production
1. Add webhook endpoint in Stripe Dashboard
2. Set endpoint URL: `https://yourdomain.com/api/webhook`
3. Select events to listen for:
   - `payment_intent.succeeded`
   - `checkout.session.completed`
4. Copy webhook signing secret to `.env`

## 🐛 Troubleshooting

### "Stripe is not defined"
- Make sure you added your publishable key in checkout-stripe.html

### Payment fails
- Check that your secret key is correct in .env
- Verify the amount is in cents (197€ = 19700 cents)

### Webhook not working
- Use `stripe listen` for local testing
- Check webhook signing secret in .env
- Verify endpoint URL is correct

## 📚 Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Node.js SDK](https://github.com/stripe/stripe-node)
- [Stripe Testing](https://stripe.com/docs/testing)
- [Stripe Webhooks](https://stripe.com/docs/webhooks)

## 🆘 Support

Bei Fragen oder Problemen:
- Email: gaertner-marcel@web.de
- Tel: +41 76 801 53 30