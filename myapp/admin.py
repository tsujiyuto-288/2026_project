from django.contrib import admin
from .models import Item, Order, ItemProcess, Process,OrderProcess

# Register your models here.
admin.site.register(Item)
admin.site.register(ItemProcess)
admin.site.register(Order)
admin.site.register(OrderProcess)
admin.site.register(Process)