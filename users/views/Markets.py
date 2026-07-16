from django.shortcuts import render,redirect
from django.views import View
from ..forms import RoleMarket
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# from django.contrib.auth.models import User
from ..models import CustomUser,Customer,Seller,Market

class CreateMarket(LoginRequiredMixin,View):
    def get(self,request):
        user = CustomUser.objects.get(user=request.user)
        if Seller.objects.filter(user=user):
            form = RoleMarket.MarketForm()
            return render(request,'users/createMarket.html',{'form':form})
        elif Customer.objects.filter(user=user) :
            message = "You are a customer! you must be a seller in order to create a market!"
            messages.error(request,message)
            return render(request,'main.html')
        else : 
            form = RoleMarket.MarketForm()
            message = "You currently don't have a role;either sign up as a seller or as a customer!"
            messages.error(request,message)
            return render(request,'users/createMarket.html',{"form":form})
    def post(self,request):
        user = CustomUser.objects.get(user=request.user)
        if Seller.objects.filter(user=user):
            seller = Seller.objects.get(user=user)
            form = RoleMarket.MarketForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                market= Market.objects.create(
                    name=form.get("name"),
                    desc=form.get("desc"),
                    address= form.get("address"),
                    phone_number= form.get("phone_number"),
                    is_active= form.get("is_active")
                )
                seller.supervisor.add(market)
                seller.markets.add(market)
                messages.success(request,"Market created succedfully!")
                return redirect('main')
            else:
                form = RoleMarket.MarketForm(request.POST)
                return render(request,'users/createMarket.html',{'form':form})
        elif Customer.objects.filter(user=user) :
            message = "You are a customer! you must be a seller in order to create a market!"
            messages.error(request,message)
            return redirect("main")
        else:
            form = RoleMarket.MarketForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                market= Market.objects.create(
                    name=form.get("name"),
                    desc=form.get("desc"),
                    address= form.get("address"),
                    phone_number= form.get("phone_number"),
                    is_active= form.get("is_active"),
                    rate=None
                )
                seller =Seller(user=user)
                seller.save()
                seller.markets.add(market)
                seller.supervisor.add(market)
                return redirect('main')
            else:
                form = RoleMarket.MarketForm(request.POST)
                return render(request,'users/createMarket.html',{'form':form})