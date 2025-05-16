from django.contrib import admin
from .models import CustomUser , Profile,Address,TechnicalComplaint,ProductComplaint
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(TechnicalComplaint)
admin.site.register(ProductComplaint)
