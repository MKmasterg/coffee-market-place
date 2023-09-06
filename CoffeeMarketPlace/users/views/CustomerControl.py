from django.views import View
from django.shortcuts import redirect,render,get_object_or_404
from ..models import Customer,CustomUser,Stock,Seller
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class CustomerMain(LoginRequiredMixin,View):
    def get(self,request):
        user = CustomUser.objects.get(user=request.user)
        customer = get_object_or_404(Customer,user=user)
        return render(request,"users/customerMain.html",{"customer":customer})

class CustomerContactInfo(LoginRequiredMixin,View):
    def get(self,request,customer_id):
        user = CustomUser.objects.get(user=request.user)
        if Seller.objects.filter(user=user).exists():
            customer = get_object_or_404(Customer,id=customer_id)
            return render(request,"users/customerContact.html",{"customer":customer})
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")

class AddToBasket(LoginRequiredMixin,View):
    def get(self,request,stock_id):
        user = CustomUser.objects.get(user=request.user)
        customer = get_object_or_404(Customer,user=user)
        stock = get_object_or_404(Stock,id=stock_id)
        if not stock in customer.basket.all():
            customer.basket.add(stock)
        else:
            messages.error(request,"Stock is already in your basket!")
            return redirect("markets:market_main",stock.market.id)
        
        messages.success(request,"Stock added to your basket successfully!")
        return redirect("markets:market_main",stock.market.id)

class RemoveFromBasket(LoginRequiredMixin,View):
    def get(self,request,stock_id):
        user = CustomUser.objects.get(user=request.user)
        customer = get_object_or_404(Customer,user=user)
        stock = get_object_or_404(Stock,id=stock_id)
        customer.basket.remove(stock)
        messages.success(request,"Stock has removed from your basket successfully!")
        return redirect(request.META['HTTP_REFERER'])