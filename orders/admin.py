from django.contrib import admin
from .models import Package, Addon, Order, OrderAddon

# Register your models here.
admin.site.register(Package)
admin.site.register(Addon)
admin.site.register(Order)
admin.site.register(OrderAddon)
