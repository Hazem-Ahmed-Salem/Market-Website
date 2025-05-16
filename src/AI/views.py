from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .ml_utils.PricePredictor import predict_price
from product.models import Product



@api_view(['POST'])
def predict_price_view(request,product_id):
    try:
        if not product_id:
            return Response({
                'error': 'Product ID is required',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        product = Product.objects.get(pk=product_id)
        product_dict = product.format_data_price_predictor()
        
        price = predict_price(product_dict)
        current_price = float(product.price)
        
        # Add some randomness for demonstration (remove in production)
        # confidence = random.randint(85, 95)
        confidence = 88
        
        return Response({
            'product_name': product.name,
            'product_id': product_id,
            'current_price': current_price,
            'predicted_price': float(f"{price:.2f}"),
            'confidence': confidence,
            'status': 'success'
        })
    except Product.DoesNotExist:
        return Response({
            'error': 'Product not found',
            'status': 'error'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e),
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)