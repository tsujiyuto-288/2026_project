from django.http import JsonResponse, HttpResponse
import json
from django.shortcuts import render
from .models import Item, Order
from django.views import View
import json


def dashbord_open(request):
    return render(request, 'dashbord.html')


class Item_register(View):
    def get(self, request):
        items = list(Item.objects.all().values())
        return render(request, 'item_register.html',{"items" : items})

    def post(self, request):
        if request.POST.get("kubun") == "save_item":
            return self.save_item(request)
        if request.POST.get("kubun") == "delete_item":
            return self.delete_item(request)
        if request.POST.get("kubun") == "get_item":
            return self.get_item(request)
        if request.POST.get("kubun") == "edit_item":
            return self.edit_item(request)

    def save_item(self, request):
        fields = json.loads(request.POST.get('fields'))

        items = Item(**fields)
        if Item.objects.filter(item_no=items.item_no).exists():
            return JsonResponse({'status': 'error_duplicate', 'message': items.item_no})
        

        
        items.save()

        return JsonResponse({'status': 'success', 'message': items.item_no})

    def delete_item(self, request):
        import json
        fields = json.loads(request.POST.get('fields'))

        item_no = fields['item_no']

        if not Item.objects.filter(item_no=item_no).exists():
            return JsonResponse({'status':'error_nai', 'message': item_no})
        
        Item.objects.filter(item_no=item_no).delete()
        
        return JsonResponse({'status': 'success', 'message': item_no})
        
    def get_item(self, request):
        items = list(Item.objects.all().values())
        return JsonResponse({'data': items})

    def edit_item(self, request):
        fields = json.loads(request.POST.get("fields"))

        if not fields.get("item_no") or not fields.get("item_name") or not fields.get("item_price"):
            return JsonResponse({"status":"kuran_error"})

        if Item.objects.filter(item_no=fields.get("item_no")).update(**fields):
            return JsonResponse({"status":"success"})
        
        return JsonResponse({"status":"error"})


class Order_input(View):
    def get(self, request):
        items = list(Item.objects.all().values())
        return render(request, 'order_input.html',{"items": items})

    def post(self, request):
        if request.POST.get("kubun") == "get_item":
            return self.get_item(request)
        if request.POST.get("kubun") == "save_order":
            return self.save_order(request)
        if request.POST.get("kubun") == "shipping_order":
            return self.shipping_order(request)
        if request.POST.get("kubun") == "delete_order":
            return self.delete_order(request)

    def save_order(self,request):
        fields = json.loads(request.POST.get('fields'))
        print(fields)

        orders = Order(**fields)

        if Order.objects.filter(order_no=orders.order_no).exists():
            return JsonResponse({'status': 'error_duplicate', 'message': orders.order_no})
        
        orders.save()

        return JsonResponse({'status': 'success', 'message': orders.order_no})

    def get_item(self,request):
        orders = list(Order.objects.filter(shipping_order=False).values())
        return JsonResponse({"data": orders})

    def shipping_order(self,request):
        shipping_order_no = request.POST.get("data")
        
        Order.objects.filter(order_no=shipping_order_no).update(shipping_order=True)
        Order.objects.filter(order_no=shipping_order_no).update(shipping_data="フロントから来た日付")#日付を入力できるようにする
        Order.objects.filter(order_no=shipping_order_no).update(shipping_quantity="フロントから来た数量")#数量をh入力できるように編集する
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


class Shipping_list(View):
    def get(self,request):
        #shippings = list(Order.objects.filter(shipping_order=True).values())
        return render(request, 'shipping_list.html')
    
    def post(self,request):
        if request.POST.get("kubun")== "get_item":
            return self.get_item(request)

    def get_item(self,request):
        shippings = list(Order.objects.filter(shipping_order=True).values())
        return JsonResponse({'data':shippings})

