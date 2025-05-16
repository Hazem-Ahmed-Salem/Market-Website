import pandas as pd
from .model_loader import ModelLoader

def predict_price(product):
    
    # Get singleton instance
    ml = ModelLoader.get_instance()
    
    # Ensure encoder is ready
    ml.ensure_encoder_fitted()
    
    # Prepare features
    features = {
        'Product_Name_Encoded': ml.label_encoder.transform([product['name']])[0],
        'Weight_Volume_g': product['Weight_Volume'],
        'Shelf_Life_Perishable': 1 if product['shelf_life'] == 'Perishable' else 0,
        'Shelf_Life_Non-Perishable': 1 if product['shelf_life'] == 'Non-Perishable' else 0,
        'Month': product['date'].month,
        'Year': product['date'].year,
        'Price': float(product['price'])
    }
    
    # Add one-hot encoded categories
    cat_encoded = ml.one_hot_encoder.transform([[product['category']]]).toarray()[0]
    for i, cat in enumerate(ml.categories):
        features[f'Category_{cat}'] = cat_encoded[i]
    
    # Predict
    input_df = pd.DataFrame([features])[ml.column_order]
    return ml.model.predict(input_df)[0]