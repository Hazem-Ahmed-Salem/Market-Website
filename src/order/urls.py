from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.shopping_cart, name='shopping_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('track/', views.order_view, name='track_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('receipt/<int:order_id>/', views.receipt, name='receipt'),
    path('accept/<int:order_id>/',views.accept_pending_order,name='accept_order'),
    path('accept-confirmed-order/<int:order_id>/',views.accept_confirmed_order,name='accept_confirmed_order'),
    path('mark-order-as-delivered/<int:order_id>/',views.mark_order_as_delivered,name='mark_delivered'),
    path('mark-order-as-cancelled/<int:order_id>/',views.mark_order_as_cancelled,name='mark_cancelled'),
    path('sales/filter/',views.filter_sales,name='filter_sales'),
]

