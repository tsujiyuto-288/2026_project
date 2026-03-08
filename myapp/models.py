from django.db import models

# 部品マスターデータ
class Item(models.Model):
    item_no = models.CharField(max_length=50,primary_key=True)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_deleted = models.BooleanField(default=False)
    item_process = models.ManyToManyField('Process', through='ItemProcess')

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
    order_no = models.CharField(max_length=50,primary_key=True)
    provisional_order = models.BooleanField(default=False)
    shipping_order = models.BooleanField(default=False)
    shipping_date = models.CharField(max_length=50)
    shipping_quantity = models.CharField(max_length=50)
    order_process = models.ManyToManyField('Process',through="OrderProcess")

# 受注データと工程の中間テーブル
class OrderProcess(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    process_turn = models.IntegerField()#工程の順番が入る(1とか2とか)

# 工程データ
class Process(models.Model):
    process_name = models.CharField(max_length=50)
    process_number = models.IntegerField()

# 作業者データ
class Employee(models.Model):
    employee_name = models.CharField(max_length=50)
    employee_number = models.IntegerField()
    retired = models.BooleanField(default=False)#退職済みの場合True