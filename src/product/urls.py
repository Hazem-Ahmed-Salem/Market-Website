from django.urls import path
from . import views
urlpatterns = [
    path('new/', views.add_products, name='add_products'),
    path('store/', views.product_preview, name='store'),
    path('add/', views.add_stock, name='add_stock'),
    path('dec/',views.decrease_stock,name='decrease_stock'),
    path('newly_added/',views.new_products_view,name='newly_added'),
    path('publish/<int:product_id>/',views.product_publish,name='product_publish'),
    path('view/<int:product_id>/',views.product_view,name='product_view'),
    path('edit/<int:product_id>/',views.product_edit,name='product_edit'),
    path('delete/<int:product_id>/',views.delete_product,name='delete_product'),
    path('wishlist/',views.wishlist_view,name='wishlist_view'),
    path('wishlist/<int:product_id>/',views.wishlist,name='wishlist'),
    path('featured/<str:category_name>/',views.all_products,name='featured_products'),
    path('update-price/<int:product_id>/',views.edit_product_price,name='edit_product_price'),
]