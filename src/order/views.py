from django.shortcuts import render,redirect
from .models import Order,CartItem
from product.models import Product
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import Address
from .models import Sales
from product.models import Product, Stock
# Create your views here.


def shopping_cart(request):
    items = CartItem.objects.filter(customer=request.user)
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'order/shopping_cart.html',{'items':items,'total_price':total_price})

@api_view(['POST'])
def remove_from_cart(request, id):
    item = CartItem.objects.get(id=id)
    if not item:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
    item.delete()
    return Response({"message": "Order removed from cart successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_to_cart(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        print("Product not found")
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    quantity = int(request.data.get('quantity'))
    if quantity  is None:
        quantity = 1
    if quantity < 0:
        quantity *= -1 
    order = CartItem.objects.create(
        product=product,
        quantity=quantity,
        customer=request.user,
        price_per_unit=product.price,
        order_price=product.price * int(quantity)
    )

    # Get updated cart count
    cart_count = CartItem.objects.filter(customer=request.user).count()
    
    return Response({
        "success": True,
        "message": "Product added to cart successfully",
        "order_id": order.id,
        "cart_count": cart_count
    }, status=status.HTTP_201_CREATED)


def order_view(request):
    orders = Order.objects.filter(customer=request.user).all()
    return render(request, 'order/order_view.html', {'orders': orders})

def checkout(request):
    addresses = Address.objects.filter(user=request.user)
    items = CartItem.objects.filter(customer=request.user)
    total_price_without_vat = float(f"{sum(item.product.price * item.quantity for item in items):.2f}")
    
    # Group duplicate items by product and sum their quantities
    grouped_items = {}
    for item in items:
        if item.product.id in grouped_items:
            grouped_items[item.product.id].quantity += item.quantity
        else:
            grouped_items[item.product.id] = item
    
    # Convert cart items to dictionary format for JSON storage
    dict_items = []
    for item in grouped_items.values():
        diction = item.to_dict()
        diction['order_price_without_vat'] = float(diction['price_per_unit']) * float(diction['quantity'])
        dict_items.append(diction)
    
    total_price = float(f"{sum(item['order_price'] for item in dict_items):.2f}")
    total_vat = float(f"{(float(total_price) - float(total_price_without_vat)):.2f}")
    
    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        delivery_address = Address.objects.get(id=address_id) if address_id else None
        
        order = Order.objects.create(
            customer=request.user,
            products=dict_items,
            order_price=total_price,
            order_price_without_vat=total_price_without_vat,
            order_vat=total_vat,
            delivery_address=delivery_address,
            payment_method=payment_method
        )
        
        # Clear the cart after creating the order
        CartItem.objects.filter(customer=request.user).delete()
        return redirect('receipt', order.id)
    
    # Get default address if available
    default_address_id = addresses.first().id if addresses.exists() else None
    
    return render(request, 'order/checkout.html', {
        'items': grouped_items.values(),
        'addresses': addresses,
        'default_address_id': default_address_id,
        'total_price': total_price,
        'total_price_without_vat': total_price_without_vat,
        'total_vat': total_vat
    })
    
    
def receipt(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order/receipt.html', {'order': order})

@api_view(['POST'])
def accept_pending_order(request,order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'confirmed'
    order.save()
    return Response({'message':'Order accepted successfully'})

@api_view(['POST'])
def accept_confirmed_order(request,order_id):
    order = Order.objects.filter(id=order_id).first()
    order.status = 'shipped'
    order.save()
    return Response({'message':'Order accepted'},status=status.HTTP_200_OK)

@api_view(['POST'])
def mark_order_as_delivered(request,order_id):
    order = Order.objects.filter(id=order_id).first()
    order.status = 'delivered'
    order.save()
    sales = Sales.objects.create(
        order=order,
        products=order.products,
        price=order.order_price
    )
    # Update product stock quantities based on the delivered order
    for item in order.products:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 0)
        
        if product_id and quantity > 0:
            try:
                product = Product.objects.get(id=product_id)
                # Get the stock object for this product
                stock = Stock.objects.filter(product=product).first()
                if stock:
                    # Deduct the ordered quantity from the stock
                    stock.quantity = max(0, stock.quantity - quantity)
                    stock.save()
            except Exception as e:
                # Log the error but continue processing
                print(f"Error updating stock for product {product_id}: {str(e)}")
    return Response({'message':'Order marked as delivered'},status=status.HTTP_200_OK)

@api_view(['POST'])
def mark_order_as_cancelled(request,order_id):
    order = Order.objects.filter(id=order_id).first()
    order.status = 'cancelled'
    order.save()
    return Response({'message':'Order marked as cancelled'},status=status.HTTP_200_OK)

@api_view(['POST'])
def filter_sales(request):
    """
    Filter sales data based on date range and category.
    Returns filtered sales data along with updated statistics and chart data.
    """
    from datetime import datetime, timedelta
    from django.db.models import Count, Sum, Avg, F
    from django.db.models.functions import TruncMonth
    
    # Get filter parameters
    date_range = request.data.get('date_range', '30')  # Default to 30 days
    category_id = request.data.get('category', 'all')
    
    # Determine the start date based on the date range
    today = datetime.now().date()
    if date_range == 'all':
        start_date = None
    else:
        try:
            days = int(date_range)
            start_date = today - timedelta(days=days)
        except ValueError:
            start_date = today - timedelta(days=30)  # Default to 30 days
    
    # Base query for sales
    sales_query = Sales.objects.all()
    
    # Apply date filter if applicable
    if start_date:
        sales_query = sales_query.filter(date__gte=start_date)
    
    # Apply category filter if applicable
    if category_id != 'all':
        # This requires parsing the products JSON field to filter by category
        # The implementation depends on how products and categories are stored
        # For now, we'll assume we can't filter by category in the database level
        # and we'll filter in memory after fetching the data
        pass
    
    # Get filtered sales
    sales = list(sales_query.order_by('-date'))
    
    # If category filter is applied, filter in memory
    if category_id != 'all':
        filtered_sales = []
        for sale in sales:
            # Check if any product in the sale belongs to the selected category
            for product in sale.products:
                product_obj = Product.objects.filter(id=product.get('product_id')).first()
                if product_obj and str(product_obj.category.id) == category_id:
                    filtered_sales.append(sale)
                    break
        sales = filtered_sales
    
    # Calculate statistics
    total_sales = sum(sale.price for sale in sales)
    orders_completed = len(sales)
    average_order_value = total_sales / orders_completed if orders_completed > 0 else 0
    
    # Find top product
    product_counts = {}
    for sale in sales:
        for product in sale.products:
            product_name = product.get('product_name')
            if product_name in product_counts:
                product_counts[product_name] += product.get('quantity', 1)
            else:
                product_counts[product_name] = product.get('quantity', 1)
    
    top_product = max(product_counts.items(), key=lambda x: x[1])[0] if product_counts else "None"
    
    # Generate monthly sales data for chart
    monthly_sales = []
    if sales:
        # Group sales by month
        sales_by_month = {}
        for sale in sales:
            month_key = sale.date.strftime('%b %Y')
            if month_key in sales_by_month:
                sales_by_month[month_key] += sale.price
            else:
                sales_by_month[month_key] = sale.price
        
        # Convert to list for chart
        for month, total in sorted(sales_by_month.items(), 
                                   key=lambda x: datetime.strptime(x[0], '%b %Y')):
            monthly_sales.append({
                'month': month,
                'total': float(total)
            })
    
    # Generate top categories data for chart
    top_categories = []
    category_counts = {}
    for sale in sales:
        for product in sale.products:
            product_obj = Product.objects.filter(id=product.get('product_id')).first()
            if product_obj:
                category_name = product_obj.category.name
                if category_name in category_counts:
                    category_counts[category_name] += product.get('quantity', 1)
                else:
                    category_counts[category_name] = product.get('quantity', 1)
    
    # Get top 5 categories
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for category_name, count in sorted_categories:
        top_categories.append({
            'name': category_name,
            'count': count
        })
    
    # Prepare sales data for response
    sales_data = []
    for sale in sales:
        sales_data.append({
            'order_id': sale.order.id,
            'date': sale.date.strftime('%Y-%m-%d'),
            'order': {
                'customer': sale.order.customer.first_name + ' ' + sale.order.customer.last_name,
                'status': sale.order.status,
                'order_price': float(sale.order.order_price)
            },
            'products': sale.products,
            'items_count': len(sale.products)
        })
    
    # Return response
    return Response({
        'sales': sales_data,
        'total_sales': float(total_sales),
        'orders_completed': orders_completed,
        'average_order_value': float(average_order_value),
        'top_product': top_product,
        'monthly_sales': monthly_sales,
        'top_categories': top_categories
    }, status=status.HTTP_200_OK)

def get_sales_dashboard_data(request):
    """
    Helper function to get sales dashboard data for the Manager template.
    This function is used by the manager_view to provide initial data for the sales dashboard.
    """
    from datetime import datetime, timedelta
    from django.db.models import Count, Sum, Avg, F
    
    # Default to last 30 days
    today = datetime.now().date()
    start_date = today - timedelta(days=30)
    
    # Get sales data
    sales = Sales.objects.filter(date__gte=start_date).order_by('-date')
    
    # Calculate statistics
    total_sales = sales.aggregate(Sum('price'))['price__sum'] or 0
    orders_completed = sales.count()
    average_order_value = total_sales / orders_completed if orders_completed > 0 else 0
    
    # Find top product
    product_counts = {}
    for sale in sales:
        for product in sale.products:
            product_name = product.get('product_name')
            if product_name in product_counts:
                product_counts[product_name] += product.get('quantity', 1)
            else:
                product_counts[product_name] = product.get('quantity', 1)
    
    top_product = max(product_counts.items(), key=lambda x: x[1])[0] if product_counts else "None"
    
    # Generate monthly sales data for chart
    monthly_sales = []
    sales_by_month = {}
    for sale in sales:
        month_key = sale.date.strftime('%b %Y')
        if month_key in sales_by_month:
            sales_by_month[month_key] += sale.price
        else:
            sales_by_month[month_key] = sale.price
    
    # Convert to list for chart
    for month, total in sorted(sales_by_month.items(), 
                               key=lambda x: datetime.strptime(x[0], '%b %Y')):
        monthly_sales.append({
            'month': month,
            'total': float(total)
        })
    
    # Generate top categories data for chart
    top_categories = []
    category_counts = {}
    for sale in sales:
        for product in sale.products:
            product_obj = Product.objects.filter(id=product.get('product_id')).first()
            if product_obj:
                category_name = product_obj.category.name
                if category_name in category_counts:
                    category_counts[category_name] += product.get('quantity', 1)
                else:
                    category_counts[category_name] = product.get('quantity', 1)
    
    # Get top 5 categories
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for category_name, count in sorted_categories:
        top_categories.append({
            'name': category_name,
            'count': count
        })
    
    return {
        'sales': sales,
        'total_sales': total_sales,
        'orders_completed': orders_completed,
        'average_order_value': average_order_value,
        'top_product': top_product,
        'monthly_sales': monthly_sales,
        'top_categories': top_categories
    }

