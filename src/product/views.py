from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import Http404
from .models import Product,Stock
from order.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from AI.ml_utils.recommender import recommend_products_for_user
import random
# Create your views here.

@api_view(['POST'])
def add_products(request):

    category = Category.objects.filter(name=request.POST.get('category')).first()
    price = float(request.POST.get('price'))
    weight= float(request.POST.get('weight'))
    volume= float(request.POST.get('volume'))
    quantity=int(request.POST.get('stock'))
    if price < 0:
        price *= -1
    if weight < 0:
        weight *= -1
    if volume < 0:
        volume *= -1
    if quantity < 0:
        quantity *= -1
    product = Product.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            price=price,
            category=category,
            image=request.FILES.get('product_image'),
            weight=weight,
            volume=volume,
        )
    stock = Stock.objects.create(
            product=product,
            quantity=quantity,
            supplier=request.POST.get('supplier'),
        )
    return Response({'message':'Product added successfully'},status=status.HTTP_200_OK)

@api_view(['POST'])
def add_stock(request):
    product = Product.objects.filter(id=request.POST.get('product')).first()
    if not product:
        raise Http404("Product not found")
    quantity = int(request.POST.get('stock'))
    if quantity < 0 :
        quantity *= -1
    stock = Stock.objects.create(
            product=product,
            quantity=quantity,
            supplier=request.POST.get('supplier'),
        )
    return Response({'message':'Stock added successfully'},status=status.HTTP_200_OK)

@api_view(['POST'])
def decrease_stock(request):
    product = Product.objects.filter(id=request.POST.get('product')).first()
    if not product:
        raise Http404("Product not found")
    stocks = Stock.objects.filter(product=product)
    decrease_amount = int(request.POST.get('quantity'))
    if decrease_amount < 0 :
        decrease_amount *= -1
    total_stock = sum(stock.quantity for stock in stocks)

    if total_stock < decrease_amount:
        raise Http404("Not enough stock available")
            
    remaining = decrease_amount
    for stock in stocks:
        if remaining <= 0:
            break
        if stock.quantity <= remaining:
            remaining -= stock.quantity
            stock.quantity = 0
            stock.delete()
        else:
            stock.quantity -= remaining
            remaining = 0
            stock.save()
    return Response({'message':'Stock decreased successfully'},status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product_name = product.name
        # Delete all stock entries for this product
        Stock.objects.filter(product=product).delete()
        # Delete the product
        product.delete()
        return Response({'message': f'Product "{product_name}" deleted successfully'}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def edit_product_price(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        # Handle JSON data from fetch API
        if request.data.get('price'):
            product.price = float(request.data.get('price'))
            if product.price < 0:
                product.price = product.price * -1
            product.save()
            return Response({'message': 'Product price updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Price is required'}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def new_products_view(request):
    products = Product.objects.filter(is_published=False)
    return render(request, 'product/new_products.html',{'products':products})

def product_preview(request):
    products = Product.objects.filter(is_published=True)
    try:
        products_ids = random.sample(list(Product.objects.filter(is_published=True).values_list('id',flat=True)),12)
        products_to_show = Product.objects.filter(id__in=products_ids)
    except Exception as e:
        print(f"Error: {e}")
        products_to_show = products[:12]
    categories = Product.get_category_choices()
    if request.user.is_authenticated:
        user_id = request.user.id
        recommended_ids = recommend_products_for_user(int(user_id),top_n=5)
        valid_recommended_ids = [id for id in recommended_ids if products.filter(id=id).exists()]
        recommended_ids = valid_recommended_ids
        recommended_products = Product.objects.filter(id__in=recommended_ids)
    else:
        recommended_ids = []
        recommended_products = []

    print(f"recommended_ids: {recommended_ids}")
    return render(request, 'product/store.html',{'products':products_to_show,'categories':categories,'recommended_products':recommended_products})

def product_edit(request,product_id):
    product = Product.objects.filter(id=product_id).first()
    category = Category.objects.filter(id=request.POST.get('category')).first()
    if not product:
        raise Http404("Product not found")
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = float(request.POST.get('price'))
        if product.price < 0:
            product.price = product.price * -1
        product.category = category
        print(request.FILES.get('image'))
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')    
        product.save()
        if request.user.user_role == 'employee':
            return redirect('employee_view') 
        elif request.user.user_role == 'manager':
            return redirect('manager_view')
        elif request.user.user_role == 'inventory_manager':
            return redirect('inventory_manager_view')
        else:
            return redirect('product_view',product_id=product_id)
    return render(request, 'product/product_edit.html',{'product':product})

def product_publish(request,product_id):
    product = Product.objects.filter(id=product_id).first()
    categories = Product.get_category_choices()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category = Category.objects.filter(name=request.POST.get('category')).first()
        product.is_published = True
        product.save()
        return redirect('employee_view')
    if not product:
        raise Http404("Product not found")
    categories = Product.get_category_choices()
    return render(request, 'product/product_publish.html',{'product':product,"categories":categories})

def product_view(request,product_id):
    product = Product.objects.filter(id=product_id).first()
    try:
        products_ids = random.sample(list(Product.objects.filter(category=product.category,is_published=True).values_list('id',flat=True)),4)
        suggested_products= Product.objects.filter(id__in=products_ids).exclude(id=product_id)
    except Exception as e:
        print(f"Error: {e}")

    if not product:
        raise Http404("Product not found")
    return render(request, 'product/product-detail.html',{'product':product,'suggested_products':suggested_products})

def wishlist_view(request):
    wishlist = request.user.wishlist_products.all()
    wishlist_count = wishlist.count()
    return render(request, 'product/favorites.html',{'wishlist_count':wishlist_count,'wishlist_items':wishlist})

@api_view(['POST'])
def wishlist(request,product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        raise Http404("Product not found")
    if product in request.user.wishlist_products.all():
        request.user.wishlist_products.remove(product)
        return Response({"message":"Product removed from wishlist",
                         "status":False},status=status.HTTP_200_OK)
    else:
        request.user.wishlist_products.add(product)
        return Response({"message":"Product added to wishlist",
                         "status":True},status=status.HTTP_200_OK)

def all_products(request,category_name):
    category = Category.objects.filter(name=category_name.title()).first()
    if category_name == 'all':
        products = Product.objects.filter(is_published=True).all()
    else:
        products = Product.objects.filter(category=category,is_published=True)
    if not category and not products:
        raise Http404("Category not found")
    categories = Product.get_category_choices()
    return render(request, 'product/all_products.html',{'products':products,'categories':categories,'category_name':category_name})

