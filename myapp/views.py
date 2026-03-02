from django.http import JsonResponse, HttpResponse
import json
from django.shortcuts import render
from .models import Item, Order, Process, ItemProcess
from django.views import View
import json


def dashbord_open(request):
    return render(request, 'dashbord.html')


class Item_register(View):
    def get(self, request):
        items = list(Item.objects.all().values())
        process_list = list(Process.objects.all().values())
        return render(request, "item_register.html", {"items": items, "process_list": process_list})

    def post(self, request):
        if request.POST.get("kubun") == "save_item":
            return self.save_item(request)
        if request.POST.get("kubun") == "delete_item":
            return self.delete_item(request)
        if request.POST.get("kubun") == "get_item":
            return self.get_item(request)
        if request.POST.get("kubun") == "edit_item":
            return self.edit_item(request)
        if request.POST.get("kubun") == "get_edit_process_list":
            return self.get_edit_process_list(request)

    def save_item(self, request):
        fields = json.loads(request.POST.get("fields"))
        process_list = json.loads(request.POST.get("process_list"))

        items = Item(**fields)
        if Item.objects.filter(item_no=items.item_no).exists():
            return JsonResponse({"status": "error_duplicate", "message": items.item_no})

        items.save()

        item_process_list = []
        for process in process_list:
            item_process = ItemProcess(
                item_id=process.get("item_no"),
                process_id=process.get("process_id"),
                process_turn=process.get("process_turn")
            )
            item_process_list.append(item_process)

        ItemProcess.objects.bulk_create(item_process_list)

        return JsonResponse({"status": "success", "message": items.item_no})

    def delete_item(self, request):
        import json
        fields = json.loads(request.POST.get('fields'))

        item_no = fields["item_no"]

        if not Item.objects.filter(item_no=item_no).exists():
            return JsonResponse({"status":"error_nai", "message": item_no})
        
        Item.objects.filter(item_no=item_no).delete()
        
        return JsonResponse({"status": "success", "message": item_no})
        
    def get_item(self, request):
        items = list(Item.objects.all().values())
        return JsonResponse({"data": items})

    def edit_item(self, request):
        fields = json.loads(request.POST.get("fields"))

        if not fields.get("item_no") or not fields.get("item_name") or not fields.get("item_price"):
            return JsonResponse({"status":"kuran_error"})

        if Item.objects.filter(item_no=fields.get("item_no")).update(**fields):
            return JsonResponse({"status":"success"})
        
        return JsonResponse({"status":"error"})

    def get_edit_process_list(self, request):
        process_list = list(Process.objects.all().values())
        return JsonResponse({"edit_process_list":process_list})

class Order_input(View):
    def get(self, request):
        items = list(Item.objects.all().values())
        return render(request, "order_input.html",{"items": items})

    def post(self, request):
        if request.POST.get("kubun") == "get_item":
            return self.get_item(request)
        if request.POST.get("kubun") == "save_order":
            return self.save_order(request)
        if request.POST.get("kubun") == "shipping_order":
            return self.shipping_order(request)
        if request.POST.get("kubun") == "delete_order":
            return self.delete_order(request)
        if request.POST.get("kubun") == "edit_order":
            return self.edit_order(request)

    def save_order(self,request):
        fields = json.loads(request.POST.get("fields"))

        orders = Order(**fields)

        if Order.objects.filter(order_no=orders.order_no).exists():
            return JsonResponse({"status": "error_duplicate", "message": orders.order_no})
        
        orders.save()

        return JsonResponse({"status": "success", "message": orders.order_no})

    def get_item(self,request):
        orders = list(Order.objects.filter(shipping_order=False).values())
        return JsonResponse({"data": orders})

    def shipping_order(self,request):
        order_content = json.loads(request.POST.get("data"))

        shipping_order_no = order_content.get("order_no")

        #仮受注の場合はエラー
        if order_content.get("provisional_order"):
            return JsonResponse({"status":"provisional_error"})

        #もし出荷済みを表す情報が送られているデータの中に含まれていたら、これ以降の処理が正しく走らないため
        if not order_content.get("shipping_order") == None:
            return JsonResponse({"status":"souteigai_error"})


        Order.objects.filter(order_no=shipping_order_no).update(shipping_order=True)
        Order.objects.filter(order_no=shipping_order_no).update(**order_content)

        return JsonResponse({"status":"success","data":shipping_order_no})
    
        
    def delete_order(self,request):
        delete_order_no = request.POST.get("data")

        delete_order = Order.objects.filter(order_no = delete_order_no)
        
        #削除対象がある時
        if delete_order:
            delete_order.delete()
            return JsonResponse({"status":"success","delete_order":delete_order_no})

        #削除対象が存在しない場合。　ただ削除対象をクリックしてここに辿り着くので削除対象がないのは何かしらの問題が起きている
        return JsonResponse({"status":"error"})

    def edit_order(self,request):
        edit_content = json.loads(request.POST.get("data"))

        Order.objects.filter(order_no=edit_content.get("order_no")).update(**edit_content)

        return JsonResponse({"status":"success"})


class Shipping_list(View):
    def get(self,request):
        return render(request, 'shipping_list.html')
    
    def post(self,request):
        if request.POST.get("kubun")== "get_item":
            return self.get_item(request)
        if request.POST.get("kubun")=="cancel_shipping":
            return self.cancel_shipping(request)

    def get_item(self,request):
        shippings = list(Order.objects.filter(shipping_order=True).values())
        return JsonResponse({"data":shippings})

    def cancel_shipping(self,request):
        cancel_order_no = request.POST.get("cancel_data")
        
        Order.objects.filter(order_no=cancel_order_no).update(shipping_order=False)

        return JsonResponse({"status":"success"})


class Process_list(View):
    def get(self,request):
        return render(request,"process_list.html")

    def post(self,request):
        if request.POST.get("kubun") == "get_item":
            return self.get_item(request)
        if request.POST.get("kubun") =="save_process":
            return self.save_process(request)
        if request.POST.get("kubun") == "edit_process":
            return self.edit_process(request)
        if request.POST.get("kubun") == "delete_process":
            return self.delete_process(request)

    def get_item(self,request):
        process_list = list(Process.objects.order_by("process_number").values())
        return JsonResponse({"data":process_list})

    def save_process(self,request):
        process = json.loads(request.POST.get("save_process"))
        
        if Process.objects.filter(process_number=process.get("process_number")):
            return JsonResponse({"status":"error_tyouhuku"})
        
        Process.objects.create(**process)
        
        return JsonResponse({"status":"success"})
    
    def edit_process(self,request):
        edit_process = json.loads(request.POST.get("edit_process"))
        
        # 変更後の工程番号が重複する場合、編集不可(自分自身を除く)
        if Process.objects.filter(process_number=edit_process.get("process_number")).exclude(id=edit_process.get("id")):
            return JsonResponse({"status":"error_tyouhuku"})
        
        Process.objects.filter(id=edit_process.get("id")).update(**edit_process)

        return JsonResponse({"status":"success"})

    def delete_process(self,request):
        delete_process = json.loads(request.POST.get("delete_process"))

        # 変更先の工程のpkが見つからない時
        if not Process.objects.filter(id=delete_process.get("id")).exists():
            return JsonResponse({"status":"error"})
        
        Process.objects.filter(id=delete_process.get("id")).delete()

        return JsonResponse({"status":"success"})
        

class progress_input(View):
    def get(self,request):
        return render(request,"progress_input.html")