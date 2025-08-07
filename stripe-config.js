// Stripe Payment Links Configuration
// Alle Payment Links für FutureCheck Produkte

const stripePaymentLinks = {
    // ========== ANALYSE-PRODUKTE (Einmalig) ==========
    'website-analyse-basic': {
        url: 'https://buy.stripe.com/7sY14n0o29ZcaOMcMI8Ra0c',
        price: 197,
        name: 'Website-Analyse Basic',
        type: 'einmalig'
    },
    'website-analyse-pro': {
        url: 'https://buy.stripe.com/14AbJ14Eifjwe0Y5kg8Ra0e', 
        price: 397,
        name: 'Website-Analyse Pro',
        type: 'einmalig'
    },
    'conversion-analyse': {
        url: 'https://buy.stripe.com/bJeaEXeeSb3g8GEbIE8Ra0d',
        price: 297,
        name: 'Conversion-Analyse',
        type: 'einmalig'
    },
    
    // ========== WEBSITE-PRODUKTE (Einmalig) ==========
    'quick-start-website': {
        url: 'https://buy.stripe.com/7sY28rb2G3AO9KIcMI8Ra0f',
        price: 497,
        name: 'Quick-Start Website',
        type: 'einmalig'
    },
    'business-website': {
        url: 'https://buy.stripe.com/28E5kDeeS9Zc4qo5kg8Ra0a',
        price: 997,
        name: 'Business Website',
        type: 'einmalig'
    },
    'professional-website': {
        url: 'https://buy.stripe.com/28E9AT3Ae5IW3mkaEA8Ra09',
        price: 1797,
        name: 'Professional Website',
        type: 'einmalig'
    },
    'e-commerce-website': {
        url: 'https://buy.stripe.com/cNi7sL5Im3AO0a8cMI8Ra0g',
        price: 2497,
        name: 'E-Commerce Website',
        type: 'einmalig'
    },
    
    // ========== SEO-PRODUKTE ==========
    'seo-starter': {
        url: 'https://buy.stripe.com/28E9AT3Ae5IW3mkaEA8Ra09',
        price: 297,
        name: 'SEO Starter',
        type: 'monatlich'
    },
    'seo-business': {
        url: 'https://buy.stripe.com/28E5kDeeS9Zc4qo5kg8Ra0a',
        price: 497,
        name: 'SEO Business',
        type: 'monatlich'
    },
    'seo-enterprise': {
        url: 'https://buy.stripe.com/bJe00j7Qu3AO7CAcMI8Ra0h',
        price: 997,
        name: 'SEO Enterprise',
        type: 'monatlich'
    },
    'local-seo-boost': {
        url: 'https://buy.stripe.com/00w6oHc6Kfjw7CAaEA8Ra06',
        price: 397,
        name: 'Local SEO Boost',
        type: 'einmalig'
    },
    'seo-komplett-setup': {
        url: 'https://buy.stripe.com/4gM4gz5Im3AO0a8bIE8Ra05',
        price: 497,
        name: 'SEO Komplett-Setup',
        type: 'einmalig'
    },
    
    // ========== MARKETING-PRODUKTE ==========
    'social-media-starter': {
        url: 'https://buy.stripe.com/8x200j3Ae3AOf527so8Ra0i',
        price: 397,
        name: 'Social Media Starter',
        type: 'monatlich'
    },
    'google-ads-management': {
        url: 'https://buy.stripe.com/3cIcN50o29Zc1ec3c88Ra0j',
        price: 497,
        name: 'Google Ads Management',
        type: 'monatlich'
    },
    'google-basis-setup': {
        url: 'https://buy.stripe.com/fZu9AT4Ei1sG3mkcMI8Ra04',
        price: 297,
        name: 'Google Basis-Setup',
        type: 'einmalig'
    },
    'full-marketing-suite': {
        url: 'https://buy.stripe.com/7sYeVd3Ae8V8f52eUQ8Ra0k',
        price: 1497,
        name: 'Full Marketing Suite',
        type: 'monatlich'
    },
    'seo-ads-komplett': {
        url: 'https://buy.stripe.com/6oU4gzfiWc7k0a8bIE8Ra0b',
        price: 797,
        name: 'SEO + Ads Komplett',
        type: 'monatlich'
    },
    
    // ========== BUNDLE-PRODUKTE (Einmalig) ==========
    'starter-bundle': {
        url: 'https://buy.stripe.com/dRm3cv8UygnAe0Y2848Ra0l',
        price: 897,
        originalPrice: 1094,
        name: 'Starter Bundle',
        type: 'einmalig'
    },
    'business-bundle': {
        url: 'https://buy.stripe.com/fZueVd9YC7R46yw9Aw8Ra0m',
        price: 1497,
        originalPrice: 1994,
        name: 'Business Bundle',
        type: 'einmalig'
    },
    'website-analyse-bundle': {
        url: 'https://buy.stripe.com/8x27sL5Im7R4e0Y2848Ra07',
        price: 1097,
        name: 'Website + Analyse Bundle',
        type: 'einmalig'
    },
    'mega-bundle': {
        url: 'https://buy.stripe.com/dRmcN5c6K2wKaOMh2Y8Ra08',
        price: 2997,
        name: 'MEGA Bundle',
        type: 'einmalig'
    },
    
    // ========== DIGITAL-ANALYSE (Legacy/Zusatz) ==========
    'futurecheck-digital-analyse-standard': {
        url: 'https://buy.stripe.com/3cIcN50o29Zc1ec3c88Ra0j',
        price: 497,
        name: 'FutureCheck Digital-Analyse - Standard',
        type: 'einmalig'
    },
    'futurecheck-digital-analyse-early-bird': {
        url: 'https://buy.stripe.com/28EaEX2wa9Zc5us9Aw8Ra03',
        price: 197,
        name: 'FutureCheck Digital-Analyse - Early Bird',
        type: 'einmalig'
    }
};

// Funktion zum Öffnen des Stripe Checkouts
function openStripeCheckout(productId) {
    const product = stripePaymentLinks[productId];
    
    if (!product) {
        console.error('Produkt nicht gefunden:', productId);
        alert('Produkt konnte nicht gefunden werden. Bitte kontaktieren Sie uns direkt.');
        return;
    }
    
    // Tracking Event (optional - für Google Analytics etc.)
    if (typeof gtag !== 'undefined') {
        gtag('event', 'begin_checkout', {
            currency: 'EUR',
            value: product.price,
            items: [{
                item_name: product.name,
                price: product.price,
                quantity: 1
            }]
        });
    }
    
    // Öffne Stripe Checkout in neuem Tab
    window.open(product.url, '_blank');
}

// Funktion zum Formatieren von Preisen
function formatPrice(price, type = 'einmalig') {
    const formatted = new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(price);
    
    return type === 'monatlich' ? `${formatted}/Monat` : formatted;
}

// Auto-Initialize wenn DOM geladen
document.addEventListener('DOMContentLoaded', function() {
    // Finde alle Buttons mit data-product-id
    const checkoutButtons = document.querySelectorAll('[data-product-id]');
    
    checkoutButtons.forEach(button => {
        const productId = button.getAttribute('data-product-id');
        
        // Click Handler hinzufügen
        button.addEventListener('click', function(e) {
            e.preventDefault();
            openStripeCheckout(productId);
        });
        
        // Optional: Hover-Effekt für bessere UX
        button.style.cursor = 'pointer';
    });
    
    // Debug Info in Console (nur in Development)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('Stripe Payment Links geladen:', Object.keys(stripePaymentLinks).length, 'Produkte');
    }
});

// Export für andere Module (falls benötigt)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { stripePaymentLinks, openStripeCheckout, formatPrice };
}