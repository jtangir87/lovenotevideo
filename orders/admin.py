from django.contrib import admin
from .models import Package, Addon, Order, OrderAddon, Payment

# Register your models here.
admin.site.register(Package)
admin.site.register(Addon)
admin.site.register(Order)
admin.site.register(OrderAddon)
admin.site.register(Payment)
