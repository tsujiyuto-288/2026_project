from django.db import models

# 部品マスターデータ
class Item(models.Model):
    item_no = models.CharField(max_length=50,primary_key=True)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_deleted = models.BooleanField(default=False)
    process_list = models.ManyToManyField('Process', through='ItemProcess')

# 部品マスターと工程の中間テーブル
class ItemProcess(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    process_turn = models.IntegerField()#工程の順番が入る(1とか2とか)

# 受注データ
class Order(models.Model):
    item_name = models.CharField(max_length=50)
    item_no = models.CharField(max_length=50)
    order_price =  models.IntegerField()
    order_no = models.CharField(max_length=50)
    provisional_order = models.BooleanField(default=False)
    shipping_order = models.BooleanField(default=False)
    shipping_date = models.CharField(max_length=50)
    shipping_quantity = models.CharField(max_length=50)

# 工程データ
class Process(models.Model):
    process_name = models.CharField(max_length=50)
    process_number = models.IntegerField()