#!/bin/bash

echo "🚀 FutureCheck Pro - Stripe Setup"
echo "================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Node.js version: $(node -v)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created from .env.example"
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file and add your Stripe keys:"
    echo "   1. STRIPE_SECRET_KEY (starts with sk_test_ or sk_live_)"
    echo "   2. STRIPE_PUBLISHABLE_KEY (starts with pk_test_ or pk_live_)"
    echo "   3. STRIPE_WEBHOOK_SECRET (starts with whsec_)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "📋 Next Steps:"
echo "=============="
echo "1. Get your Stripe keys from https://dashboard.stripe.com/apikeys"
echo "2. Edit the .env file and add your keys"
echo "3. Update checkout-stripe.html line 509 with your publishable key"
echo "4. Run 'npm run dev' to start the development server"
echo "5. Open http://localhost:3001 in your browser"
echo ""
echo "🔧 Stripe Webhook Setup (for production):"
echo "   stripe listen --forward-to localhost:3001/api/webhook"
echo ""
echo "✨ Setup complete!"