/**
 * ShopEasy Global E-Commerce Utilities
 * Consolidated helper functions for CSRF, Wishlist, Cart & Toast Notifications
 */

// Helper to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    // Fallback: check meta tag
    if (!cookieValue) {
        const metaCsrf = document.querySelector('meta[name="csrf-token"]');
        if (metaCsrf) {
            cookieValue = metaCsrf.getAttribute('content');
        }
    }
    return cookieValue;
}

// Global modern toast notification (matching 404.html aesthetic)
function showNotification(message, type = 'info') {
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'notification-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `notification-toast toast-${type}`;
    
    let iconClass = 'fa-info-circle';
    if (type === 'success') iconClass = 'fa-circle-check';
    else if (type === 'error') iconClass = 'fa-circle-exclamation';
    else if (type === 'warning') iconClass = 'fa-triangle-exclamation';

    toast.innerHTML = `
        <div class="toast-icon"><i class="fas ${iconClass}"></i></div>
        <div class="toast-body">${message}</div>
        <button type="button" class="toast-close" aria-label="Close" onclick="this.closest('.notification-toast').remove()">&times;</button>
    `;

    container.appendChild(toast);

    // Auto dismiss after 3.8s
    setTimeout(() => {
        toast.classList.add('toast-hiding');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 3800);
}

// Global Wishlist toggle handler
function addToWishlist(event, productId) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    const wishlistIcon = event ? (event.currentTarget || event.target.closest('.wishlist-icon') || event.target.closest('.btn-wishlist-float')) : null;
    const csrfToken = getCookie('csrftoken');

    const wasActive = wishlistIcon ? wishlistIcon.classList.contains('active') : false;

    // Optimistic UI toggle
    if (wishlistIcon) {
        if (wasActive) {
            wishlistIcon.classList.remove('active');
        } else {
            wishlistIcon.classList.add('active');
        }
    }

    fetch(`/product/wishlist/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'added') {
            if (wishlistIcon) wishlistIcon.classList.add('active');
            showNotification(data.message || 'Product added to wishlist!', 'success');
        } else if (data.status === 'removed') {
            if (wishlistIcon) wishlistIcon.classList.remove('active');
            showNotification(data.message || 'Product removed from wishlist!', 'success');
        } else {
            showNotification(data.message || 'Wishlist updated', 'info');
        }
    })
    .catch(error => {
        console.error('Wishlist error:', error);
        // Revert toggle
        if (wishlistIcon) {
            if (wasActive) {
                wishlistIcon.classList.add('active');
            } else {
                wishlistIcon.classList.remove('active');
            }
        }
        showNotification('Unable to update wishlist. Please try again.', 'error');
    });
}

// Global Add to Cart handler
function addToCart(event, productId, button) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    if (!button) return;
    
    const originalHtml = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    const csrfToken = getCookie('csrftoken');

    fetch(`/order/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ quantity: 1 })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success || data.cart_count !== undefined) {
            // Update all cart count badges in headers
            const cartCountElements = document.querySelectorAll('.cart-count');
            cartCountElements.forEach(el => {
                el.textContent = data.cart_count;
            });
            button.innerHTML = '<i class="fas fa-check"></i> Added!';
            button.style.backgroundColor = '#2ecc71';
            showNotification('Added to cart successfully!', 'success');
            setTimeout(() => {
                button.innerHTML = originalHtml;
                button.disabled = false;
                button.style.backgroundColor = '';
            }, 1800);
        } else {
            button.innerHTML = originalHtml;
            button.disabled = false;
            showNotification(data.message || 'Could not add to cart.', 'error');
        }
    })
    .catch(error => {
        console.error('Add to cart error:', error);
        button.innerHTML = originalHtml;
        button.disabled = false;
        showNotification('Please login to add items to your cart.', 'error');
    });
}
