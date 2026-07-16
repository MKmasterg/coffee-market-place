from django.views import View
from users.models import Order,Stock,Customer,CustomUser
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

class PlaceOrder(LoginRequiredMixin,View):
    # return redirect(request.META['HTTP_REFERER'])
    def get(self,request):
        user = CustomUser.objects.get(user=request.user)
        customer = get_object_or_404(Customer,user=user)
        if customer.basket.all():
            stocks= []
            for each in customer.basket.all():
                if each.is_available:
                    stocks.append(each)
            if stocks:
                return render(request,"markets/placeOrder.html",{"stocks":stocks})
            else:
                messages.error(request,"All of your items in basket are not available at this moment.")
                return redirect("users:customer_pf")  
        else:
            messages.error(request,"You can't place order with empty basket, can you?!")
            return redirect("users:customer_pf")
    
    def post(self,request):
        user = CustomUser.objects.get(user=request.user)
        customer = get_object_or_404(Customer,user=user)
        stocks= []
        for each in customer.basket.all():
            if each.is_available:
                stocks.append(each)
        errors = []
        for key,value in request.POST.dict().items():
            if "stock" in key:
                id = int(key[5:])
                for each in stocks:
                    if id == each.id:
                        break
                else:
                    messages.error(request,"Something's wrong.")
                    return render(request,"markets/placeOrder.html",{"stocks":stocks})
                
                stock = Stock.objects.get(id=id)
                if int(value) > stock.no:
                    errors.append(id)
        if errors :
            for id in errors:
                messages.error(request,f"The number of order of stock no {id} is more than market's inventory")
            else:
                return render(request,"markets/placeOrder.html",{"stocks":stocks})
        else:
            for key,value in request.POST.dict().items():
                if "stock" in key:
                    id = int(key[5:])
                    msg = request.POST.get(f"msg{id}")
                    if msg != None and len(msg) <= 200: 
                        stock = Stock.objects.get(id=id)
                        Order.objects.create(
                            stock=stock,
                            customer=customer,
                            market=stock.market,
                            number_of_stock=int(value),
                            date_placed=datetime.datetime.now(),
                            status=300,
                            message=msg
                        )
                        remained = stock.no - int(value)
                        Stock.objects.filter(id=id).update(no=remained)
                        if remained == 0 :
                            Stock.objects.filter(id=id).update(is_available=False)
                    else:
                        messages.error(request,"The messages' length should be less than 200 characters")
                        return render(request,"markets/placeOrder.html",{"stocks":stocks})
            else:
                customer.basket.clear()
                messages.success(request,"Your order has been placed!")
                return redirect("users:customer_pf")