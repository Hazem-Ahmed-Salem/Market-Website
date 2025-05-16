import joblib
import json
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np
import os
from django.conf import settings

class ModelLoader:
    _instance = None
    
    def __init__(self):
        if ModelLoader._instance is not None:
            raise Exception("Singleton class - use get_instance()")
        
        # Load ML files
        model_path = os.path.join(settings.BASE_DIR, 'AI', 'ml_models', 'price_prediction_model.pkl')
        self.model = joblib.load(model_path)
        
        col_path = os.path.join(settings.BASE_DIR, 'AI', 'ml_models', 'column_order.json')
        with open(col_path) as f:
            self.column_order = json.load(f)
        
        # Initialize encoders
        self.categories = ['Dairy', 'Beverages', 'Snacks', 'Fruits', 'Vegetables']
        self.one_hot_encoder = OneHotEncoder(handle_unknown='ignore')
        self.one_hot_encoder.fit([[cat] for cat in self.categories])
        
        # Load recommendation system 
        self.label_encoder = LabelEncoder()
        self._label_encoder_fitted = False
        self.svd = joblib.load(os.path.join(settings.BASE_DIR, 'AI', 'ml_models', 'svd_model.pkl'))
        self.product_ids = np.load(os.path.join(settings.BASE_DIR, 'AI', 'ml_models', 'user_product_matrix_columns.npy'), allow_pickle=True)
        self.user_ids = np.load(os.path.join(settings.BASE_DIR, 'AI', 'ml_models', 'user_product_matrix_index.npy'), allow_pickle=True)
        self.user_product_matrix = np.load(os.path.join(settings.BASE_DIR, 'AI', 'ml_models', 'user_product_matrix.npy'), allow_pickle=True)
        
        ModelLoader._instance = self
    
    def ensure_encoder_fitted(self):
        if not self._label_encoder_fitted:
            from product.models import Product
            names = list(Product.objects.values_list('name', flat=True))
            if names:
                self.label_encoder.fit(names)
                self._label_encoder_fitted = True
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelLoader()
        return cls._instance