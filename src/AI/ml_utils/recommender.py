import numpy as np
import random
import logging
from typing import List, Union
from .model_loader import ModelLoader
from product.models import Product

logger = logging.getLogger(__name__)

def recommend_products_for_user(user_id: Union[int, str], top_n: int = 5) -> List[int]:
    """
    Returns list of recommended product IDs for the given user.
    Handles new users by returning random products.
    """
    try:
        # Ensure consistent type handling
        user_id = int(user_id)
        ml = ModelLoader.get_instance()
        
        # Debug: Verify model loading
        if not hasattr(ml, 'svd') or not hasattr(ml, 'product_ids'):
            logger.error("Recommendation model not properly loaded!")
            return _get_fallback_products(top_n)

        # Convert numpy arrays to Python types for comparison
        existing_user_ids = [int(x) for x in ml.user_ids]
        
        # Handle new users
        if user_id not in existing_user_ids:
            logger.info(f"New user {user_id}, returning random products")
            return _get_fallback_products(top_n)

        # Get user index and ratings
        user_idx = np.where(ml.user_ids == user_id)[0]
        if len(user_idx) == 0:
            logger.warning(f"User {user_id} not found in matrix despite check")
            return _get_fallback_products(top_n)
            
        user_ratings = ml.user_product_matrix[user_idx[0]]
        
        # Generate predictions
        try:
            user_transformed = ml.svd.transform(user_ratings.reshape(1, -1))
            predicted_scores = np.dot(user_transformed, ml.svd.components_)[0]
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return _get_fallback_products(top_n)

        # Filter out already rated products
        predicted_scores[user_ratings > 0] = -np.inf
        
        # Get top N recommendations
        top_indices = np.argsort(predicted_scores)[::-1][:top_n]
        recommended_ids = [int(ml.product_ids[i]) for i in top_indices]
        
        # Verify IDs exist in database
        valid_ids = list(Product.objects.filter(id__in=recommended_ids).values_list('id', flat=True))
        final_ids = [pid for pid in recommended_ids if pid in valid_ids]
        
        # If we lost too many recommendations, fill with fallback
        if len(final_ids) < top_n:
            logger.warning(f"Only found {len(final_ids)}/{top_n} valid products")
            final_ids.extend(_get_fallback_products(top_n - len(final_ids)))
            
        return final_ids[:top_n]

    except Exception as e:
        logger.exception("Recommendation failed completely")
        return _get_fallback_products(top_n)

def _get_fallback_products(count: int) -> List[int]:
    """Returns random product IDs from database"""
    try:
        available_ids = list(Product.objects.values_list('id', flat=True))
        return random.sample(available_ids, min(count, len(available_ids))) if available_ids else []
    except Exception as e:
        logger.error(f"Fallback products failed: {str(e)}")
        return []