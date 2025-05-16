from django.urls import path
from . import views
urlpatterns = [
    path('manager/',views.Manager_view,name='manager_view'),
    path('inventory-manager/',views.inventory_manager_view,name='inventory_manager_view'),
    path('employee/',views.employee_view,name='employee_view'),
    path('driver/',views.driver_view,name='driver_view'),
]