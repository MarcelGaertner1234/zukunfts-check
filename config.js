// Configuration for FutureCheck MVP
// Replace these with your actual keys when setting up

const config = {
    // Formspree Configuration (NEW - SUPER EASY!)
    formspree: {
        formId: 'movlkqpp', // Your actual Formspree form ID
        // Form is active and ready to receive submissions!
    },
    
    // Stripe Configuration
    stripe: {
        // Use Stripe Payment Links (no backend needed!)
        paymentLink: 'https://buy.stripe.com/test_5kQeV60d8f5r4Rg77H7bW01', // Early Bird 197€
        paymentLinkRegular: 'https://buy.stripe.com/test_dRm00c7FA9L7abA8bL7bW02', // Regular Price 497€
        currentPrice: 'earlyBird', // Switch to 'regular' after 20 customers
        successUrl: '/danke.html',
        cancelUrl: '/checkout.html'
    },
    
    // Business Configuration
    pricing: {
        regularPrice: 497,
        earlyBirdPrice: 197,
        currency: 'EUR',
        spotsAvailable: 20
    },
    
    // Contact Information
    contact: {
        email: 'gaertner-marcel@web.de',
        phone: '+41 76 801 53 30',
        company: 'FutureCheck',
        address: 'Michelsrotweg 6, 74821 Mosbach'
    },
    
    // Feature Flags
    features: {
        demoMode: false, // LIVE MODE - Everything is active!
        formspreeEnabled: true, // Formspree is configured and ready!
        stripeEnabled: true, // Stripe is NOW ACTIVE! Payment Link ready!
        analyticsEnabled: false // Enable for tracking
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
}