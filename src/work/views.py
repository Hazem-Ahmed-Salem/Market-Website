from django.shortcuts import render,redirect
from product.models import Product
from order.models import Order,Sales
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import ProductComplaint,TechnicalComplaint
from rest_framework import status
# Create your views here.

def landing(request):
    return redirect('store')

def Manager_view(request):
    if not request.user.is_authenticated:
        return redirect('store')
    if request.user.user_role != 'manager':
        return redirect(f'{request.user.user_role}_view')
    products = Product.objects.all()
    product_complaints = ProductComplaint.objects.all()
    categories = Product.get_category_choices()
    sales = Sales.objects.all()
    total_sales = float(f"{Sales.objects.aggregate(total_sales=Sum('price'))['total_sales']:.2f}")
    orders_completed = Order.objects.filter(status='delivered').count()
    average_order_value = float(f"{(total_sales / orders_completed if orders_completed > 0 else 0):.2f}")
    # Calculate top ordered products from delivered orders
    top_products = {}
    delivered_orders = Order.objects.filter(status='delivered')
    
    # Iterate through delivered orders and count product occurrences
    for order in delivered_orders:
        for product_data in order.products:
            product_name = product_data.get('product_name', '')
            if product_name:
                if product_name in top_products:
                    top_products[product_name] += 1
                else:
                    top_products[product_name] = 1
    
    # Sort products by order count (descending)
    top_ordered_products = sorted(
        [{'name': name, 'count': count} for name, count in top_products.items()],
        key=lambda x: x['count'],
        reverse=True
    )
    # Calculate top ordered categories from delivered orders
    category_counts = {}
    
    # Iterate through delivered orders and count category occurrences
    for order in delivered_orders:
        for product_data in order.products:
            category_name = product_data.get('product_category', '')
            if category_name:
                if category_name in category_counts:
                    category_counts[category_name] += 1
                else:
                    category_counts[category_name] = 1
    
    # Sort categories by order count (descending)
    top_ordered_categories = sorted(
        [{'name': name, 'count': count} for name, count in category_counts.items()],
        key=lambda x: x['count'],
        reverse=True
    )
    
    top_category = top_ordered_categories[0]['name'] if top_ordered_categories else 'None'
    top_product = top_ordered_products[0]['name'] if top_ordered_products else 'None'
    
    # Generate monthly sales data for chart
    monthly_sales = []
    from datetime import datetime
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
    
    return render(request, 'work/manager.html',{'products':products,
                                                'product_complaints':product_complaints,
                                                'sales':sales,
                                                'total_sales':total_sales,
                                                'orders_completed':orders_completed,
                                                'average_order_value':average_order_value,
                                                'top_product':top_product,
                                                'top_categories':top_ordered_categories,
                                                'monthly_sales':monthly_sales,
                                                'categories':categories})

def inventory_manager_view(request):
    if not request.user.is_authenticated:
        return redirect('store')
    if request.user.user_role != 'inventory_manager':
        return redirect(f'{request.user.user_role}_view')
    products = Product.objects.all()
    categories = Product.get_category_choices()
    pending_orders = Order.objects.filter(status='pending').all()
    return render(request, 'work/inv_manager.html',{'products':products,'categories':categories,'pending_orders':pending_orders})


def employee_view(request):
    if not request.user.is_authenticated:
        return redirect('store')
    if request.user.user_role != 'employee':
        return redirect(f'{request.user.user_role}_view')
    products = Product.objects.filter(is_published=True).all()
    new_products = Product.objects.filter(is_published=False).all()
    print(new_products)
    categories = Product.get_category_choices()
    technical_complaints = TechnicalComplaint.objects.all()
    return render(request, 'work/employee.html',{'products':products,'new_products':new_products,'categories':categories,'technical_complaints':technical_complaints})

def driver_view(request):
    if not request.user.is_authenticated:
        return redirect('store')
    if request.user.user_role != 'driver':
        return redirect(f'{request.user.user_role}_view')
    confirmed_orders = Order.objects.filter(status='confirmed').all()
    active_orders = Order.objects.filter(status='shipped').all()
    cancelled_orders = Order.objects.filter(status='cancelled').all()
    delivered_orders = Order.objects.filter(status='delivered').all()
    return render(request, 'work/driver.html',{'confirmed_orders':confirmed_orders,'active_orders':active_orders,'cancelled_orders':cancelled_orders,'delivered_orders':delivered_orders})

