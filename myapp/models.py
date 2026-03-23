from django.db import models

# 部品マスターデータ
class Item(models.Model):
    item_no = models.CharField(
        verbose_name="品番",
        max_length=50,
    )
    item_name = models.CharField(
        verbose_name="品名",
        max_length=50,
        default="",
    )
    item_price = models.IntegerField(
        verbose_name="単価",
        null=True,
        blank=True,
    )
    item_deleted = models.BooleanField(
        verbose_name="廃番",
        default=False
    )
    item_note = models.TextField(
        verbose_name="備考",
        default="",
    )
    item_process = models.ManyToManyField(
        "Process", 
        verbose_name="標準実施工程",
        through="ItemProcess",
    )

# 部品マスターと工程の中間テーブル
class ItemProcess(models.Model):
    itemprocess_item = models.ForeignKey(
        "Item",
        verbose_name="品番",
        on_delete=models.PROTECT
    )
    itemprocess_process = models.ForeignKey(
        "Process",
        verbose_name="工程",
        on_delete=models.PROTECT
    )
    itemprocess_turn = models.IntegerField(
        verbose_name="順番"
    )

# 得意先
class Customer(models.Model):
    customer_name = models.CharField(
        max_length=50,
        verbose_name="得意先名",
    )
    customer_code = models.CharField(
        max_length=50,
        verbose_name="得意先コード",
    )
    customer_address = models.CharField(
        max_length=100,
        verbose_name="得意先住所",
        default=""
    )
    customer_telnumber = models.CharField(
        max_length=50,
        verbose_name="電話番号",
        default=""
    )
    customer_delivery = models.CharField(
        max_length=50,
        verbose_name="納入先名",
        default="",
    )
    customer_deliveryaddress = models.CharField(
        max_length=100,
        verbose_name="納入先住所",
        default="",
    )
    customer_note = models.TextField(
        default="",
        verbose_name="備考"
    )

# 受注データ
class Order(models.Model):
    order_item = models.ForeignKey(
        "Item",
        verbose_name="品番",
        on_delete=models.PROTECT,
    )
    order_customer = models.ForeignKey(
        "Customer",
        verbose_name="得意先",
        on_delete=models.PROTECT
    )
    order_price =  models.IntegerField(
        verbose_name="受注単価",
        null=True,
        blank=True,
    )
    order_quantity = models.IntegerField(
        verbose_name="受注数",
        null=True,
        blank=True,
    )
    order_no = models.CharField(
        max_length=50,
        verbose_name="受注番号",
        default="",
    )
    order_provisional = models.BooleanField(
        verbose_name="仮受注",
        default=False
    )
    order_deadline = models.DateField(
        verbose_name="納期",
        null=True,
        blank=True,
    )
    order_note = models.TextField(
        verbose_name="備考",
        default="",
    )

# 出荷
class Shipping(models.Model):
    SHIPPING_TYPE_CHOICES = [
        ["complete","完納"],
        ["partial","分納"],
        ["discontinued","打切"],
    ]

    shipping_order = models.ForeignKey(
        "Order",
        verbose_name="受注",
        on_delete=models.PROTECT
    )

    shipping_date = models.DateField(
        verbose_name="出荷日",
        null=True,
        blank=True,
    )

    shipping_quantity = models.IntegerField(
        verbose_name="出荷数",
        null=True,
        blank=True,
    )

    shipping_type = models.CharField(
        max_length=20,
        verbose_name="出荷区分",
        default="",
        choices=SHIPPING_TYPE_CHOICES
    )

    shipping_employee = models.ForeignKey(
        "Employee",
        verbose_name="出荷担当者",
        on_delete=models.PROTECT
    )

    shipping_note = models.TextField(
        verbose_name="備考",
        default="",
    )

# 生産指示
class Instructions(models.Model):
    instructions_no = models.CharField(
        max_length=10,
        verbose_name="生産No",
    )

    instructions_deadline = models.DateField(
        verbose_name="生産納期",
        null=True,
        blank=True,
    )

    instructions_employee = models.ForeignKey(
        "Employee",
        verbose_name="生産担当者",
        on_delete=models.PROTECT
    )

    instructions_quantity = models.IntegerField(
        verbose_name="生産数",
        null=True,
        blank=True,
    )

    instructions_item = models.ForeignKey(
        "Item",
        verbose_name="品番",
        on_delete=models.PROTECT
    )

    instructions_note = models.TextField(
        verbose_name="備考",
        default="",
    )

# 工程データ
class Process(models.Model):
    process_name = models.CharField(
        max_length=50,
        verbose_name="工程名",
    )

    process_sort = models.IntegerField(
        verbose_name="順番",
    )

# 社員データ
class Employee(models.Model):
    employee_name = models.CharField(
        max_length=50,
        verbose_name="社員名",
    )

    employee_code = models.CharField(
        max_length=10,
        verbose_name="社員コード",
    )

    employee_retired = models.BooleanField(
        verbose_name="退職",
        default=False
    )

# 生産工程
class ProductionProcess(models.Model):
    productionprocess_instructions = models.ForeignKey(
        "Instructions",
        verbose_name="生産指示",
        on_delete=models.PROTECT
    )

    productionprocess_process = models.ForeignKey(
        "Process",
        verbose_name="工程",
        on_delete=models.PROTECT
    )

    productionprocess_turn = models.IntegerField(
        verbose_name="順番",
    )

# 進捗データ
class Progress(models.Model):
    progress_productionprocess = models.ForeignKey(
        "ProductionProcess",
        verbose_name="生産工程",
        on_delete=models.PROTECT
    )

    progress_employee = models.ForeignKey(
        "Employee",
        verbose_name="作業者",
        on_delete=models.PROTECT
    )

    progress_date = models.DateField(
        verbose_name="作業日",
    )

    progress_quantity = models.IntegerField(
        verbose_name="数量",
    )

    progress_note = models.TextField(
        verbose_name="備考",
        default="",
    )

    progress_defective = models.BooleanField(
        verbose_name="不良",
        default=False
    )
    
# 引当(在庫と出荷)
class Allocation(models.Model):
    allocation_order = models.ForeignKey(
        "Order",
        verbose_name="受注",
        on_delete=models.PROTECT
    )

    allocation_progress = models.ForeignKey(
        "Progress",
        verbose_name="進捗",
        on_delete=models.PROTECT
    )

    allocation_quantity = models.IntegerField(
        verbose_name="引当数",
    )