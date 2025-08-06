require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet({
    contentSecurityPolicy: false, // Disable for development
}));

// CORS configuration
app.use(cors({
    origin: ['http://localhost:3000', 'http://localhost:3001', 'https://zukunfts-check.com', 'file://*'],
    credentials: true
}));

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname, '..')));

// Stripe API routes - Alte Payment Links (backup)
const stripeApiRoutes = require('./stripe-api');
app.use('/api/old', stripeApiRoutes);

// Neue Stripe Checkout Integration
const stripeCheckoutRoutes = require('./stripe-checkout');
app.use('/api/stripe', stripeCheckoutRoutes);

// Email service - mit Fallback
let sendCustomerDataEmail;
try {
    const emailService = require('./email-service');
    sendCustomerDataEmail = emailService.sendCustomerDataEmail;
} catch (error) {
    console.warn('Email service not available, using mock');
    const emailMock = require('./email-mock');
    sendCustomerDataEmail = emailMock.sendCustomerDataEmail;
}

// Send customer data email
app.post('/api/send-customer-data', async (req, res) => {
    try {
        const customerData = req.body;
        
        // Validate required fields
        if (!customerData.email || !customerData.firstName || !customerData.lastName) {
            return res.status(400).json({ 
                error: 'Missing required fields' 
            });
        }
        
        const result = await sendCustomerDataEmail(customerData);
        
        if (result.success) {
            res.json({ 
                success: true, 
                message: 'Customer data email sent successfully',
                messageId: result.messageId
            });
        } else {
            res.status(500).json({ 
                error: 'Failed to send email',
                details: result.error
            });
        }
        
    } catch (error) {
        console.error('Error in send-customer-data endpoint:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: error.message
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        stripe: !!process.env.STRIPE_SECRET_KEY 
    });
});

// Serve HTML files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'index.html'));
});

app.get('/checkout', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'checkout-stripe.html'));
});

app.get('/danke', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'danke.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        error: 'Something went wrong!',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
});

// Start server
app.listen(PORT, () => {
    console.log(`
    🚀 Server is running!
    📍 Local: http://localhost:${PORT}
    🔑 Stripe: ${process.env.STRIPE_SECRET_KEY ? '✅ Configured' : '❌ Not configured'}
    🌍 Environment: ${process.env.NODE_ENV || 'development'}
    `);
});