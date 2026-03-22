from django.contrib import admin
from .models import (
    Item, Order, Customer, ItemProcess, Process, Employee,
    Shipping,Instructions,ProductionProcess,Progress,Allocation
    )

admin.site.register(Item)
admin.site.register(ItemProcess)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Shipping)
admin.site.register(Instructions)
admin.site.register(ProductionProcess)
admin.site.register(Progress)
admin.site.register(Allocation)
admin.site.register(Process)
admin.site.register(Employee)