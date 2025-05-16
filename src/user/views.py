from django.shortcuts import render,redirect
from django.contrib.auth import login,logout, authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Profile,Address,TechnicalComplaint,ProductComplaint
from product.models import Product
from order.models import Order
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


def login_signup_view(request):
    return render(request, 'user/login_signup.html')

def logout_view(request):
    logout(request)
    return redirect('login_signup')

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            return Response({
                'success': False,
                'message': 'Please provide both email and password'
            }, status=400)
            
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'message': 'Login successful',
                'redirect_url': reverse('profile')
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid email or password'
            }, status=401)

def signup_view(request):
    email = request.POST['email']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    user_model = get_user_model()
    user = user_model.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
    login(request, user)
    return redirect('next_register')

def next_register_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please login first.')
        return redirect('login_signup')
    
    # Check if user already has a profile
    # try:
    #     if request.user.profile:
    #         return redirect('profile')
    # except Profile.DoesNotExist:
    #     pass  
    
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        profile_picture = request.FILES.get('profile_picture')
        
        # Get address fields
        address_type = request.POST['address_type']
        address = request.POST['address']
        apartment = request.POST.get('apartment', '')  # Optional field
        city = request.POST['city']
        governorate = request.POST['governorate']

        if not profile_picture:
            profile_picture = 'profile_pictures/default.svg'
        
        user = request.user
        
        # Create address
        address = Address.objects.create(
            user=user,
            address_type=address_type,
            address=address,
            apartment=apartment,
            city=city,
            governorate=governorate
        )
        
        # Create profile
        Profile.objects.create(
            user=user,
            gender=gender,
            phone_number=phone_number,
            profile_picture=profile_picture
        )
        
        messages.success(request, 'Profile completed successfully!')
        return redirect('profile')
        
    return render(request, 'user/next_register_page.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login_signup')
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('next_register')
    orders = Order.objects.filter(customer=request.user)
    orders_count = orders.count()
    addresses = Address.objects.filter(user=request.user)
    addresses_count = addresses.count()
    wishlist = Product.objects.filter(wishlist=request.user)
    wishlist_count = wishlist.count()
    return render(request, 'user/profile.html', {'orders': orders, 'orders_count': orders_count, 'addresses': addresses, 'addresses_count': addresses_count, 'wishlist': wishlist, 'wishlist_count': wishlist_count})

def complaint_view(request):
    if not request.user.is_authenticated:
        return redirect('login_signup')
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('next_register')
    return render(request, 'user/complaint.html')

@api_view(['POST'])
def profile_edit_view(request):
    if request.method == 'POST':
        try:
            data = request.data
            action = data.get('action')

            if action == 'update_profile':
                # Update user fields
                if 'first_name' in data:
                    request.user.first_name = data['first_name']
                if 'last_name' in data:
                    request.user.last_name = data['last_name']
                if 'email' in data:
                    request.user.email = data['email']
                request.user.save()

                # Update profile fields
                try:
                    profile = request.user.profile
                except Profile.DoesNotExist:
                    profile = Profile.objects.create(user=request.user)

                if 'phone_number' in data:
                    profile.phone_number = data['phone_number']
                if 'gender' in data:
                    profile.gender = data['gender']
                
                # Handle profile picture update
                if 'profile_picture' in request.FILES:
                    # Delete old profile picture if it exists
                    if profile.profile_picture:
                        old_image_path = profile.profile_picture.path
                        if os.path.isfile(old_image_path):
                            os.remove(old_image_path)
                    profile.profile_picture = request.FILES['profile_picture']
                
                profile.save()

                return Response({
                    'success': True,
                    'message': 'Profile updated successfully',
                    'user': {
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'email': request.user.email,
                        'profile': {
                            'phone_number': profile.phone_number,
                            'gender': profile.gender,
                            'profile_picture': profile.profile_picture.url if profile.profile_picture else None
                        }
                    }
                })

            elif action == 'change_password':
                current_password = data.get('current_password')
                new_password = data.get('new_password')
                confirm_password = data.get('confirm_password')

                if not all([current_password, new_password, confirm_password]):
                    return Response({
                        'success': False,
                        'error': 'All password fields are required'
                    }, status=400)

                if new_password != confirm_password:
                    return Response({
                        'success': False,
                        'error': 'New passwords do not match'
                    }, status=400)

                # Verify current password
                if not request.user.check_password(current_password):
                    return Response({
                        'success': False,
                        'error': 'Current password is incorrect'
                    }, status=400)

                # Set new password
                request.user.set_password(new_password)
                request.user.save()
                
                return Response({
                    'success': True,
                    'message': 'Password changed successfully'
                })

            else:
                return Response({
                    'success': False,
                    'error': 'Invalid action'
                }, status=400)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)

    return Response({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)

@api_view(['POST'])
def add_address_view(request):
    if request.method == 'POST':
        try:
            # Get data from request.data instead of request.body
            data = request.data
            address_type = data.get('address_type')
            apartment = data.get('apartment')
            address = data.get('address')
            city = data.get('city')
            governorate = data.get('governorate')

            # Validate required fields
            if not all([address_type, address, city, governorate]):
                return Response({
                    'success': False,
                    'error': 'Missing required fields'
                }, status=400)

            # Create the address
            new_address = Address.objects.create(
                user=request.user,
                address_type=address_type,
                apartment=apartment,
                address=address,
                city=city,
                governorate=governorate
            )

            return Response({
                'success': True,
                'message': 'Address added successfully',
                'address': {
                    'address_type': new_address.address_type,
                    'address': new_address.address,
                    'apartment': new_address.apartment,
                    'city': new_address.city,
                    'governorate': new_address.governorate
                },
                'user': {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'profile': {
                        'phone_number': request.user.profile.phone_number
                    }
                }
            }, status=200)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return Response({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)

@api_view(['POST'])
def edit_address_view(request, address_id):
    if request.method == 'POST':
        try:
            # Get the address
            address = Address.objects.get(id=address_id, user=request.user)
            
            # Get data from request
            data = request.data
            address_type = data.get('address_type')
            apartment = data.get('apartment')
            address_text = data.get('address')
            city = data.get('city')
            governorate = data.get('governorate')

            # Validate required fields
            if not all([address_type, address_text, city, governorate]):
                return Response({
                    'success': False,
                    'error': 'Missing required fields'
                }, status=400)

            # Update the address
            address.address_type = address_type
            address.apartment = apartment
            address.address = address_text
            address.city = city
            address.governorate = governorate
            address.save()

            return Response({
                'success': True,
                'message': 'Address updated successfully',
                'address': {
                    'id': address.id,
                    'address_type': address.address_type,
                    'address': address.address,
                    'apartment': address.apartment,
                    'city': address.city,
                    'governorate': address.governorate
                },
                'user': {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'profile': {
                        'phone_number': request.user.profile.phone_number
                    }
                }
            }, status=200)
        except Address.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Address not found'
            }, status=404)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return Response({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)

@api_view(['POST'])
def delete_address_view(request, address_id):
    if request.method == 'POST':
        try:
            # Get the address
            address = Address.objects.get(id=address_id, user=request.user)
            
            # Delete the address
            address.delete()

            return Response({
                'success': True,
                'message': 'Address deleted successfully'
            }, status=200)
        except Address.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Address not found'
            }, status=404)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return Response({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)


@api_view(['POST'])
def submit_technical_complaint(request):
    if request.method == 'POST':
        try:
            data = request.data
            page_url = data.get('page_url')
            issue_type = data.get('issue_type')
            complaint_description = data.get('complaint_description')
            issue_image = data.get('issue_image')
        except Exception as e:
            print(e)
        technical_complaint = TechnicalComplaint.objects.create(
            user=request.user,
            page_url=page_url,
            issue_type=issue_type,
            complaint_description=complaint_description,
            issue_image=issue_image
        )
        return Response({
            'success': True,
            'message': 'Technical complaint submitted successfully'
        }, status=200)


@api_view(['POST'])
def submit_product_complaint(request):
    if request.method == 'POST':
        try:
            data = request.data
            issue_type = data.get('issue_type')
            order_number = data.get('order_number')
            product_name = data.get('product_name')
            product_image = data.get('issue_image')
            complaint_description = data.get('complaint_description')
        except Exception as e:
            print(e)
        product_complaint = ProductComplaint.objects.create(
            user=request.user,
            issue_type=issue_type,
            order_number=order_number,
            product_name=product_name,
            product_image=product_image,
            complaint_description=complaint_description
        )
        return Response({
            'success': True,
            'message': 'Product complaint submitted successfully'
        }, status=200)  

@api_view(['POST'])
def delete_product_complaint(request, complaint_id):
    try:
        complaint = ProductComplaint.objects.get(id=complaint_id)
        complaint.delete()
        return Response({
            'success': True,
            'message': 'Product complaint deleted successfully'
        }, status=200)
    except ProductComplaint.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Product complaint not found'
        }, status=404)

@api_view(['POST'])
def delete_technical_complaint(request, complaint_id):
    try:
        complaint = TechnicalComplaint.objects.get(id=complaint_id)
        complaint.delete()  
        return Response({
            'success': True,
            'message': 'Technical complaint deleted successfully'
        }, status=200)
    except TechnicalComplaint.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Technical complaint not found'
        }, status=404)



