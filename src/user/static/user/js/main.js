// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart count
    updateCartCount();
    
    // Initialize modals
    initModals();
    
    // Initialize product tabs
    initProductTabs();
    
    // Initialize FAQ accordion
    initFAQAccordion();
    
    // Initialize thumbnail image switching
    initThumbnailImages();
    
    // Initialize profile tabs
    initProfileTabs();
    
    // Initialize checkout steps
    initCheckoutSteps();
    
    // Toggle billing address
    toggleBillingAddress();
    
    // Show order number field when relevant subject is selected
    showOrderNumberField();
});

// Update cart count in header
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCountElements = document.querySelectorAll('.cart-count');
    
    cartCountElements.forEach(element => {
        element.textContent = cart.reduce((total, item) => total + item.quantity, 0);
    });
}

// Initialize modals
function initModals() {
    const loginBtn = document.getElementById('login-btn');
    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    const showRegister = document.getElementById('show-register');
    const showLogin = document.getElementById('show-login');
    const closeModalButtons = document.querySelectorAll('.close-modal');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loginModal.style.display = 'flex';
        });
    }
    
    if (showRegister) {
        showRegister.addEventListener('click', function(e) {
            e.preventDefault();
            loginModal.style.display = 'none';
            registerModal.style.display = 'flex';
        });
    }
    
    if (showLogin) {
        showLogin.addEventListener('click', function(e) {
            e.preventDefault();
            registerModal.style.display = 'none';
            loginModal.style.display = 'flex';
        });
    }
    
    closeModalButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
}

// Initialize product tabs
function initProductTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and panes
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });
            
            // Add active class to clicked button and corresponding pane
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Initialize FAQ accordion
function initFAQAccordion() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            this.classList.toggle('active');
            const answer = this.nextElementSibling;
            answer.classList.toggle('active');
        });
    });
}

// Initialize thumbnail image switching
function initThumbnailImages() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('main-product-image');
    
    if (thumbnails.length && mainImage) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                mainImage.src = this.src;
            });
        });
    }
}

// Initialize profile tabs
function initProfileTabs() {
    const profileMenuLinks = document.querySelectorAll('.profile-menu a');
    
    profileMenuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href').substring(1);
            
            // Remove active class from all links and sections
            document.querySelectorAll('.profile-menu a').forEach(item => {
                item.parentElement.classList.remove('active');
            });
            
            document.querySelectorAll('.profile-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Add active class to clicked link and corresponding section
            this.parentElement.classList.add('active');
            document.getElementById(sectionId).classList.add('active');
        });
    });
}

// Initialize checkout steps
function initCheckoutSteps() {
    const steps = document.querySelectorAll('.step');
    
    steps.forEach(step => {
        step.addEventListener('click', function() {
            const stepNumber = this.getAttribute('data-step');
            // In a real implementation, this would navigate to the corresponding step
            console.log(`Navigating to step ${stepNumber}`);
        });
    });
}

// Toggle billing address
function toggleBillingAddress() {
    const checkbox = document.getElementById('different-billing');
    const billingAddress = document.getElementById('billing-address');
    
    if (checkbox && billingAddress) {
        checkbox.addEventListener('change', function() {
            billingAddress.style.display = this.checked ? 'block' : 'none';
        });
    }
}

// Show order number field when relevant subject is selected
function showOrderNumberField() {
    const subjectSelect = document.getElementById('contact-subject');
    const orderNumberGroup = document.getElementById('order-number-group');
    
    if (subjectSelect && orderNumberGroup) {
        subjectSelect.addEventListener('change', function() {
            const relevantSubjects = ['order', 'delivery', 'product', 'return'];
            orderNumberGroup.style.display = relevantSubjects.includes(this.value) ? 'block' : 'none';
        });
    }
}

// Helper function to format price
function formatPrice(price) {
    return '$' + parseFloat(price).toFixed(2);
}