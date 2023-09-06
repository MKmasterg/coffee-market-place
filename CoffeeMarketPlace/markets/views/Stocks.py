from django.views import View
from users.models import Seller,CustomUser,Market,Stock
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,get_object_or_404
from ..forms import StocksForms


class StockRegistration(LoginRequiredMixin,View):
    def get(self,request,market_id):
        user = CustomUser.objects.get(user=request.user)
        seller = get_object_or_404(Seller,user=user)
        market = get_object_or_404(Market,id=market_id)
        if seller in market.markets_seller_set.all():
            form = StocksForms.StockRegistrationForm()
            return render(request,"markets/stockRegistration.html",{"form":form})
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")
        
    def post(self,request,market_id):
        user = CustomUser.objects.get(user=request.user)
        seller = get_object_or_404(Seller,user=user)
        market = get_object_or_404(Market,id=market_id)
        if seller in market.markets_seller_set.all():
            form = StocksForms.StockRegistrationForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                Stock.objects.create(
                    name= form.get("name"),
                    desc= form.get("desc"),
                    no= form.get("no"),
                    is_available= form.get("is_available"),
                    market= market,
                    ppg= form.get("ppg")
                    
                )
                messages.success(request,"Stock registered successfully!")
                return redirect("markets:market_main",market_id)

            else:
                return render(request,"markets/stockRegistration.html",{"form":form})

        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")
        
class StockDeletion(LoginRequiredMixin,View):
    def get(self,request,stock_id):
        user = CustomUser.objects.get(user=request.user)
        seller = get_object_or_404(Seller,user=user)
        stock = get_object_or_404(Stock,id=stock_id)
        market_id = stock.market.id
        if stock.market in seller.markets.all() :
            stock.delete()
            messages.success(request,"Stock removed successfully!")
            return redirect("markets:market_main",market_id)
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")
        
class StockModification(LoginRequiredMixin,View):
    def get(self,request,stock_id):
        user = CustomUser.objects.get(user=request.user)
        seller = get_object_or_404(Seller,user=user)
        stock = get_object_or_404(Stock,id=stock_id)
        if stock.market in seller.markets.all() :
            payload={
                "name":stock.name,
                "desc":stock.desc,
                "no":stock.no,
                "is_available":stock.is_available,
                "ppg":stock.ppg
            }
            form = StocksForms.StockRegistrationForm(payload)
            return render(request,"markets/stockRegistration.html",{"form":form})
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")
    def post(self,request,stock_id):
        user = CustomUser.objects.get(user=request.user)
        seller = get_object_or_404(Seller,user=user)
        stock = get_object_or_404(Stock,id=stock_id)
        if stock.market in seller.markets.all():
            form = StocksForms.StockRegistrationForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                Stock.objects.filter(id=stock_id).update(
                    name= form.get("name"),
                    desc= form.get("desc"),
                    no= form.get("no"),
                    is_available= form.get("is_available"),
                    ppg= form.get("ppg")
                )
                messages.success(request,"Stock modified successfully!")
                return redirect("markets:market_main",stock.market.id)

            else:
                return render(request,"markets/stockRegistration.html",{"form":form})

        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")