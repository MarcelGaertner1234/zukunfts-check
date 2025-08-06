// Mock Email Service für Testing
const sendCustomerDataEmail = async (customerData) => {
    console.log('Email would be sent to:', customerData.email);
    console.log('Customer:', customerData.firstName, customerData.lastName);
    console.log('Company:', customerData.company);
    console.log('Product:', customerData.productName);
    
    return {
        success: true,
        messageId: 'mock-' + Date.now(),
        message: 'Email mock successful'
    };
};

module.exports = {
    sendCustomerDataEmail
};