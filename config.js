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
        // LIVE Stripe Payment Links - ECHTE ZAHLUNGEN!
        paymentLink: 'https://buy.stripe.com/cNi9AT0o20oC9KIeUQ8Ra00', // Early Bird 197€ LIVE
        paymentLinkRegular: 'https://buy.stripe.com/14AfZh3Ae1sGbSQfYU8Ra01', // Regular Price 497€ LIVE
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