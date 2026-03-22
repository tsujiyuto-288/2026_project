from django.db import models

# 部品マスターデータ
class Item(models.Model):
    item_no = models.CharField(max_length=50)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_deleted = models.BooleanField(default=False)
    item_note = models.TextField()
    item_process = models.ManyToManyField("Process", through="ItemProcess")

# 部品マスターと工程の中間テーブル
class ItemProcess(models.Model):
    itemprocess_item = models.ForeignKey("Item", on_delete=models.PROTECT)
    itemprocess_process = models.ForeignKey("Process", on_delete=models.PROTECT)
    itemprocess_turn = models.IntegerField()

# 得意先
class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    customer_code = models.CharField(max_length=50)
    customer_address = models.CharField(max_length=100)
    customer_telnumber = models.CharField(max_length=50)
    customer_delivery = models.CharField(max_length=50)
    customer_deliveryaddress = models.CharField(max_length=100)
    customer_note = models.TextField()

# 受注データ
class Order(models.Model):
    order_item = models.ForeignKey("Item", on_delete=models.PROTECT)
    order_customer = models.ForeignKey("Customer", on_delete=models.PROTECT)
    order_price =  models.IntegerField()
    order_quantity = models.IntegerField()
    order_no = models.CharField(max_length=50)
    order_provisional = models.BooleanField(default=False)
    order_deadline = models.DateField()
    order_note = models.TextField()

# 出荷
class Shipping(models.Model):
    SHIPPING_TYPE_CHOICES = [
        ["complete","完納"],
        ["partial","分納"],
        ["discontinued","打切"],
    ]
    shipping_order = models.ForeignKey("Order", on_delete=models.PROTECT)
    shipping_date = models.DateField()
    shipping_quantity = models.IntegerField()
    shipping_type = models.CharField(max_length=20,choices=SHIPPING_TYPE_CHOICES)
    shipping_employee = models.ForeignKey("Employee", on_delete=models.PROTECT)
    shipping_note = models.TextField()

# 生産指示
class Instructions(models.Model):
    instructions_no = models.CharField(max_length=10)
    instructions_deadline = models.DateField()
    instructions_employee = models.ForeignKey("Employee", on_delete=models.PROTECT)
    instructions_quantity = models.IntegerField()
    instructions_item = models.ForeignKey("Item", on_delete=models.PROTECT)
    instructions_note = models.TextField()

# 工程データ
class Process(models.Model):
    process_name = models.CharField(max_length=50)
    process_sort = models.IntegerField()#表示順

# 社員データ
class Employee(models.Model):
    employee_name = models.CharField(max_length=50)
    employee_code = models.CharField(max_length=10)
    employee_retired = models.BooleanField(default=False)#退職済みの場合True

# 生産工程
class ProductionProcess(models.Model):
    productionprocess_instructions = models.ForeignKey("Instructions", on_delete=models.PROTECT)
    productionprocess_process = models.ForeignKey("Process", on_delete=models.PROTECT)
    productionprocess_turn = models.IntegerField()

# 進捗データ
class Progress(models.Model):
    progress_productionprocess = models.ForeignKey("ProductionProcess", on_delete=models.PROTECT)
    progress_employee = models.ForeignKey("Employee", on_delete=models.PROTECT)
    progress_date = models.DateField()
    progress_quantity = models.IntegerField()
    progress_note = models.TextField()
    progress_defective = models.BooleanField(default=False)
    
# 引当(在庫と出荷)
class Allocation(models.Model):
    allocation_order = models.ForeignKey("Order", on_delete=models.PROTECT)
    allocation_progress = models.ForeignKey("Progress", on_delete=models.PROTECT)
    allocation_quantity = models.IntegerField()