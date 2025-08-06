const express = require('express');
const router = express.Router();
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Create payment intent
router.post('/create-payment-intent', async (req, res) => {
    try {
        const { amount, customer } = req.body;
        
        // Validate amount
        if (!amount || amount < 100) {
            return res.status(400).json({ 
                error: 'Invalid amount' 
            });
        }
        
        // Create or retrieve customer
        let stripeCustomer;
        try {
            // Check if customer exists
            const customers = await stripe.customers.list({
                email: customer.email,
                limit: 1
            });
            
            if (customers.data.length > 0) {
                stripeCustomer = customers.data[0];
            } else {
                // Create new customer
                stripeCustomer = await stripe.customers.create({
                    email: customer.email,
                    name: customer.name,
                    phone: customer.phone,
                    address: customer.address,
                    metadata: customer.metadata
                });
            }
        } catch (customerError) {
            console.error('Customer creation error:', customerError);
            stripeCustomer = null;
        }
        
        // Create payment intent
        const paymentIntent = await stripe.paymentIntents.create({
            amount: amount, // Amount in cents
            currency: 'eur',
            customer: stripeCustomer?.id,
            description: customer.metadata?.product || 'FutureCheck Pro Service',
            metadata: {
                ...customer.metadata,
                customer_email: customer.email,
                customer_name: customer.name
            },
            automatic_payment_methods: {
                enabled: true,
            },
        });
        
        res.json({
            clientSecret: paymentIntent.client_secret,
            customerId: stripeCustomer?.id
        });
        
    } catch (error) {
        console.error('Payment intent error:', error);
        res.status(500).json({ 
            error: error.message || 'Failed to create payment intent' 
        });
    }
});

// Create checkout session (alternative method)
router.post('/create-checkout-session', async (req, res) => {
    try {
        const { productId, successUrl, cancelUrl } = req.body;
        
        // Define products
        const products = {
            'analysis': {
                name: 'Website-Analyse',
                price: 19700, // in cents
                description: 'Detaillierte Website-Analyse mit 30-seitigem Report'
            },
            'website-quick': {
                name: 'Website Quick-Start',
                price: 49700,
                description: 'Professionelle Website mit bis zu 5 Seiten'
            },
            'website-business': {
                name: 'Website Business',
                price: 99700,
                description: 'Business Website mit bis zu 10 Seiten und Blog'
            },
            'website-professional': {
                name: 'Website Professional',
                price: 179700,
                description: 'Premium Website mit unbegrenzten Seiten'
            },
            'seo-setup': {
                name: 'SEO Setup',
                price: 29700,
                description: 'Einmalige SEO-Optimierung'
            },
            'seo-monthly': {
                name: 'SEO Betreuung',
                price: 29700,
                description: 'Monatliche SEO-Betreuung',
                recurring: true
            },
            'bundle': {
                name: 'MEGA-BUNDLE',
                price: 199700,
                description: 'Website Business + SEO Setup + 3 Monate Betreuung'
            }
        };
        
        const product = products[productId] || products['analysis'];
        
        // Create line items
        const lineItems = [{
            price_data: {
                currency: 'eur',
                product_data: {
                    name: product.name,
                    description: product.description,
                },
                unit_amount: product.price,
                ...(product.recurring && {
                    recurring: {
                        interval: 'month'
                    }
                })
            },
            quantity: 1,
        }];
        
        // Create checkout session
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card', 'sepa_debit'],
            line_items: lineItems,
            mode: product.recurring ? 'subscription' : 'payment',
            success_url: successUrl || `${process.env.DOMAIN}/danke.html?success=true&session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: cancelUrl || `${process.env.DOMAIN}/checkout-stripe.html?canceled=true`,
            automatic_tax: { enabled: true },
            allow_promotion_codes: true,
            billing_address_collection: 'required',
            customer_email: req.body.customerEmail,
            metadata: {
                productId: productId,
                ...req.body.metadata
            }
        });
        
        res.json({ 
            sessionId: session.id,
            url: session.url 
        });
        
    } catch (error) {
        console.error('Checkout session error:', error);
        res.status(500).json({ 
            error: error.message || 'Failed to create checkout session' 
        });
    }
});

// Webhook handler for Stripe events
router.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;
    
    let event;
    
    try {
        event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
    } catch (err) {
        console.error('Webhook signature verification failed:', err);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }
    
    // Handle the event
    switch (event.type) {
        case 'payment_intent.succeeded':
            const paymentIntent = event.data.object;
            console.log('PaymentIntent was successful!', paymentIntent);
            // TODO: Fulfill the order, send email, etc.
            await handleSuccessfulPayment(paymentIntent);
            break;
            
        case 'checkout.session.completed':
            const session = event.data.object;
            console.log('Checkout session completed!', session);
            // TODO: Fulfill the order
            await handleCompletedCheckout(session);
            break;
            
        case 'customer.subscription.created':
            const subscription = event.data.object;
            console.log('Subscription created!', subscription);
            // TODO: Handle new subscription
            break;
            
        default:
            console.log(`Unhandled event type ${event.type}`);
    }
    
    res.json({ received: true });
});

// Helper functions
async function handleSuccessfulPayment(paymentIntent) {
    try {
        const { sendPaymentConfirmationEmail } = require('./email-service');
        
        const paymentData = {
            paymentId: paymentIntent.id,
            amount: paymentIntent.amount / 100,
            product: paymentIntent.metadata?.product || paymentIntent.description,
            customerEmail: paymentIntent.metadata?.customer_email || 'Nicht verfügbar'
        };
        
        // E-Mail an dich senden
        await sendPaymentConfirmationEmail(paymentData);
        
        console.log('Processing successful payment:', paymentData);
        
    } catch (error) {
        console.error('Error handling successful payment:', error);
    }
}

async function handleCompletedCheckout(session) {
    try {
        const { sendPaymentConfirmationEmail } = require('./email-service');
        
        const paymentData = {
            paymentId: session.id,
            amount: session.amount_total / 100,
            product: session.metadata?.productId || 'Nicht spezifiziert',
            customerEmail: session.customer_details?.email || session.customer_email || 'Nicht verfügbar'
        };
        
        // E-Mail an dich senden
        await sendPaymentConfirmationEmail(paymentData);
        
        console.log('Processing completed checkout:', paymentData);
        
    } catch (error) {
        console.error('Error handling completed checkout:', error);
    }
}

// Get payment status
router.get('/payment-status/:paymentIntentId', async (req, res) => {
    try {
        const paymentIntent = await stripe.paymentIntents.retrieve(
            req.params.paymentIntentId
        );
        
        res.json({
            status: paymentIntent.status,
            amount: paymentIntent.amount / 100,
            currency: paymentIntent.currency,
            created: paymentIntent.created
        });
        
    } catch (error) {
        console.error('Error retrieving payment status:', error);
        res.status(404).json({ 
            error: 'Payment not found' 
        });
    }
});

module.exports = router;