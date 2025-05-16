// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Load featured products on homepage
    if (document.getElementById('featured-products')) {
        loadFeaturedProducts();
    }
    
    // Load all products on products page
    if (document.getElementById('products-container')) {
        loadAllProducts();
    }
    
    // Load related products on product detail page
    if (document.getElementById('related-products')) {
        loadRelatedProducts();
    }
    
    // Initialize product filters
    initProductFilters();
    
    // Initialize product pagination
    initProductPagination();
});

// Sample product data
const products = [
    {
        id: 1,
        name: 'Premium Wireless Headphones',
        price: 199.99,
        originalPrice: 249.99,
        image: 'images/Screenshot (79).png',
        category: 'electronics',
        rating: 4.5,
        reviews: 120,
        description: 'Experience premium sound quality with our wireless headphones. Featuring noise cancellation, 30-hour battery life, and comfortable over-ear design.',
        features: [
            'Active Noise Cancellation',
            '30-hour battery life',
            'Bluetooth 5.0',
            'Built-in microphone',
            'Foldable design'
        ]
    },
    {
        id: 2,
        name: 'Smart Watch Pro',
        price: 249.99,
        image: 'images/Screenshot (79).png',
        category: 'electronics',
        rating: 4.2,
        reviews: 85,
        description: 'Stay connected with our advanced smart watch featuring health tracking, notifications, and long battery life.',
        features: [
            'Heart rate monitor',
            'Sleep tracking',
            'Water resistant',
            '7-day battery life',
            'Customizable watch faces'
        ]
    },
    {
        id: 3,
        name: 'Wireless Earbuds',
        price: 79.99,
        originalPrice: 99.99,
        image: 'images/Screenshot (79).png',
        category: 'electronics',
        rating: 4.0,
        reviews: 65,
        description: 'Compact wireless earbuds with crystal clear sound and comfortable fit.',
        features: [
            'Bluetooth 5.0',
            '20-hour battery with case',
            'Touch controls',
            'IPX5 water resistant',
            'Noise isolation'
        ]
    },
    {
        id: 4,
        name: 'Fitness Tracker',
        price: 49.99,
        image: 'images/Screenshot (79).png',
        category: 'electronics',
        rating: 3.8,
        reviews: 42,
        description: 'Track your daily activity and workouts with this lightweight fitness tracker.',
        features: [
            'Step counter',
            'Calorie tracker',
            'Sleep monitoring',
            '30-day battery life',
            'Smart notifications'
        ]
    },
    {
        id: 5,
        name: 'Men\'s Running Shoes',
        price: 89.99,
        image: 'images/Screenshot (79).png',
        category: 'fashion',
        rating: 4.3,
        reviews: 78,
        description: 'Lightweight running shoes with superior cushioning and support.',
        features: [
            'Breathable mesh upper',
            'Cushioned midsole',
            'Flexible outsole',
            'Arch support',
            'Multiple color options'
        ]
    },
    {
        id: 6,
        name: 'Women\'s Yoga Pants',
        price: 39.99,
        image: 'images/Screenshot (79).png',
        category: 'fashion',
        rating: 4.6,
        reviews: 112,
        description: 'Comfortable and stylish yoga pants for workouts or casual wear.',
        features: [
            'High-waisted design',
            'Stretchy fabric',
            'Moisture-wicking',
            'Pockets',
            'Multiple sizes'
        ]
    },
    {
        id: 7,
        name: 'Blender',
        price: 59.99,
        image: 'images/Screenshot (79).png',
        category: 'home',
        rating: 4.1,
        reviews: 53,
        description: 'Powerful blender for smoothies, soups, and more.',
        features: [
            '1000W motor',
            '6-speed settings',
            'BPA-free pitcher',
            'Easy clean',
            '2-year warranty'
        ]
    },
    {
        id: 8,
        name: 'Air Fryer',
        price: 99.99,
        image: 'images/Screenshot (79).png',
        category: 'home',
        rating: 4.4,
        reviews: 91,
        description: 'Healthy cooking with little to no oil using this versatile air fryer.',
        features: [
            '5.8L capacity',
            'Digital controls',
            '8 presets',
            'Non-stick basket',
            'Auto shut-off'
        ]
    },
    {
        id: 9,
        name: 'Facial Cleanser',
        price: 24.99,
        image: 'images/Screenshot (79).png',
        category: 'beauty',
        rating: 4.7,
        reviews: 134,
        description: 'Gentle yet effective facial cleanser for all skin types.',
        features: [
            'pH balanced',
            'Dermatologist tested',
            'No parabens',
            'No sulfates',
            'Vegan formula'
        ]
    },
    {
        id: 10,
        name: 'Hair Dryer',
        price: 69.99,
        image: 'images/Screenshot (79).png',
        category: 'beauty',
        rating: 4.0,
        reviews: 47,
        description: 'Professional hair dryer with multiple heat and speed settings.',
        features: [
            '1875W motor',
            '3 heat settings',
            '2 speed settings',
            'Cool shot button',
            'Concentrator nozzle'
        ]
    }
];

// Load featured products on homepage
function loadFeaturedProducts() {
    const featuredProductsContainer = document.getElementById('featured-products');
    const featuredProducts = products.slice(0, 4); // Get first 4 products as featured
    
    featuredProductsContainer.innerHTML = featuredProducts.map(product => `
        <div class="product-card">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}">
                ${product.originalPrice ? '<span class="product-badge">Sale</span>' : ''}
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <div class="price">
                    <span class="current-price">${formatPrice(product.price)}</span>
                    ${product.originalPrice ? `<span class="original-price">${formatPrice(product.originalPrice)}</span>` : ''}
                    ${product.originalPrice ? `<span class="discount">${Math.round((1 - product.price / product.originalPrice) * 100)}% OFF</span>` : ''}
                </div>
                <div class="rating">
                    ${generateStarRating(product.rating)}
                    <span>(${product.reviews})</span>
                </div>
                <div class="product-actions">
                    <button class="btn-add-to-cart" data-id="${product.id}">Add to Cart</button>
                    <button class="btn-wishlist" data-id="${product.id}"><i class="far fa-heart"></i></button>
                </div>
            </div>
        </div>
    `).join('');
    
    // Add event listeners to buttons
    addProductEventListeners();
}

// Load all products on products page
function loadAllProducts(filteredProducts = products) {
    const productsContainer = document.getElementById('products-container');
    
    productsContainer.innerHTML = filteredProducts.map(product => `
        <div class="product-card">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}">
                ${product.originalPrice ? '<span class="product-badge">Sale</span>' : ''}
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <div class="price">
                    <span class="current-price">${formatPrice(product.price)}</span>
                    ${product.originalPrice ? `<span class="original-price">${formatPrice(product.originalPrice)}</span>` : ''}
                    ${product.originalPrice ? `<span class="discount">${Math.round((1 - product.price / product.originalPrice) * 100)}% OFF</span>` : ''}
                </div>
                <div class="rating">
                    ${generateStarRating(product.rating)}
                    <span>(${product.reviews})</span>
                </div>
                <div class="product-actions">
                    <button class="btn-add-to-cart" data-id="${product.id}">Add to Cart</button>
                    <button class="btn-wishlist" data-id="${product.id}"><i class="far fa-heart"></i></button>
                </div>
            </div>
        </div>
    `).join('');
    
    // Add event listeners to buttons
    addProductEventListeners();
    
    // Update pagination info
    updatePaginationInfo();
}

// Load related products on product detail page
function loadRelatedProducts() {
    const relatedProductsContainer = document.getElementById('related-products');
    const relatedProducts = products.slice(4, 8); // Get some products as related
    
    relatedProductsContainer.innerHTML = relatedProducts.map(product => `
        <div class="product-card">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}">
                ${product.originalPrice ? '<span class="product-badge">Sale</span>' : ''}
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <div class="price">
                    <span class="current-price">${formatPrice(product.price)}</span>
                    ${product.originalPrice ? `<span class="original-price">${formatPrice(product.originalPrice)}</span>` : ''}
                    ${product.originalPrice ? `<span class="discount">${Math.round((1 - product.price / product.originalPrice) * 100)}% OFF</span>` : ''}
                </div>
                <div class="rating">
                    ${generateStarRating(product.rating)}
                    <span>(${product.reviews})</span>
                </div>
                <div class="product-actions">
                    <button class="btn-add-to-cart" data-id="${product.id}">Add to Cart</button>
                    <button class="btn-wishlist" data-id="${product.id}"><i class="far fa-heart"></i></button>
                </div>
            </div>
        </div>
    `).join('');
    
    // Add event listeners to buttons
    addProductEventListeners();
}

// Initialize product filters
function initProductFilters() {
    const categoryFilter = document.getElementById('category-filter');
    const sortBy = document.getElementById('sort-by');
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            filterProducts();
        });
    }
    
    if (sortBy) {
        sortBy.addEventListener('change', function() {
            filterProducts();
        });
    }
}

// Filter and sort products
function filterProducts() {
    const categoryFilter = document.getElementById('category-filter');
    const sortBy = document.getElementById('sort-by');
    
    let filteredProducts = [...products];
    
    // Filter by category
    if (categoryFilter && categoryFilter.value !== 'all') {
        filteredProducts = filteredProducts.filter(product => product.category === categoryFilter.value);
    }
    
    // Sort products
    if (sortBy) {
        switch (sortBy.value) {
            case 'price-low':
                filteredProducts.sort((a, b) => a.price - b.price);
                break;
            case 'price-high':
                filteredProducts.sort((a, b) => b.price - a.price);
                break;
            case 'rating':
                filteredProducts.sort((a, b) => b.rating - a.rating);
                break;
            case 'newest':
                // Assuming newer products have higher IDs
                filteredProducts.sort((a, b) => b.id - a.id);
                break;
            default:
                // Default sorting (by ID)
                filteredProducts.sort((a, b) => a.id - b.id);
        }
    }
    
    loadAllProducts(filteredProducts);
}

// Initialize product pagination
function initProductPagination() {
    const prevPage = document.getElementById('prev-page');
    const nextPage = document.getElementById('next-page');
    
    if (prevPage) {
        prevPage.addEventListener('click', function() {
            // In a real implementation, this would load the previous page
            console.log('Loading previous page');
        });
    }
    
    if (nextPage) {
        nextPage.addEventListener('click', function() {
            // In a real implementation, this would load the next page
            console.log('Loading next page');
        });
    }
}

// Update pagination info
function updatePaginationInfo() {
    const pageInfo = document.getElementById('page-info');
    
    if (pageInfo) {
        // In a real implementation, this would show actual pagination info
        pageInfo.textContent = 'Page 1 of 5';
    }
}

// Add event listeners to product buttons
function addProductEventListeners() {
    // Add to cart buttons
    document.querySelectorAll('.btn-add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.getAttribute('data-id'));
            addToCart(productId);
        });
    });
    
    // Wishlist buttons
    document.querySelectorAll('.btn-wishlist').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.getAttribute('data-id'));
            addToWishlist(productId);
        });
    });
}

// Add product to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Check if product already in cart
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            quantity: 1
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    
    // Show success message
    alert(`${product.name} has been added to your cart!`);
}

// Add product to wishlist
function addToWishlist(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    
    // Check if product already in wishlist
    const existingItem = wishlist.find(item => item.id === productId);
    
    if (!existingItem) {
        wishlist.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image
        });
        
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        
        // Show success message
        alert(`${product.name} has been added to your wishlist!`);
    } else {
        // Show already in wishlist message
        alert(`${product.name} is already in your wishlist!`);
    }
}

// Generate star rating HTML
function generateStarRating(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    let stars = '';
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }
    
    // Half star
    if (hasHalfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }
    
    // Empty stars
    for (let i = 0; i < emptyStars; i++) {
        stars += '<i class="far fa-star"></i>';
    }
    
    return stars;
}