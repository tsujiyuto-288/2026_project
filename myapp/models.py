from django.db import models

# Create your models here.

class Item(models.Model):
    item_no = models.CharField(max_length=50)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_deleted = models.BooleanField(default=False)
    process_list = models.JSONField(blank=True,null=True)#空欄を許可

class Order(models.Model):
    item_name = models.CharField(max_length=50)
    item_no = models.CharField(max_length=50)
    order_price =  models.IntegerField()
    order_no = models.CharField(max_length=50)
    provisional_order = models.BooleanField(default=False)
    shipping_order = models.BooleanField(default=False)
    shipping_date = models.CharField(max_length=50)
    shipping_quantity = models.CharField(max_length=50)


class Process(models.Model):
    process_name = models.CharField(max_length=50)
    process_number = models.IntegerField()
