from django.urls import path
from . import views
urlpatterns = [
    path('login_signup/', views.login_signup_view, name='login_signup'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('next_register/', views.next_register_view, name='next_register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('add-address/', views.add_address_view, name='add_address'),
    path('edit-address/<int:address_id>/', views.edit_address_view, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address_view, name='delete_address'),
    path('submit-technical-complaint/', views.submit_technical_complaint, name='submit_technical_complaint'),
    path('submit-product-complaint/', views.submit_product_complaint, name='submit_product_complaint'),
    path('delete-product-complaint/<int:complaint_id>/', views.delete_product_complaint, name='delete_product_complaint'),
    path('delete-technical-complaint/<int:complaint_id>/', views.delete_technical_complaint, name='delete_technical_complaint'),
] 