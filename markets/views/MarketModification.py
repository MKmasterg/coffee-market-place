from django import views
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from users.models import Market,CustomUser,Seller
from users.forms import MarketForm


class MarketEdit(LoginRequiredMixin,views.View):
    def get(self,request,market_id):
        user = CustomUser.objects.get(user=request.user)
        market = get_object_or_404(Market,id=market_id)
        if Seller.objects.filter(user=user):
            seller = Seller.objects.get(user=user)
            if market in seller.supervisor.all():
                payload={
                    'name':market.name,
                    'desc':market.desc,
                    'address':market.address,
                    'phone_number':market.phone_number,
                    'is_active':market.is_active
                }
                form = MarketForm(payload)
                return render(request,'markets/marketModification.html',{'form':form})
            else:
                messages.error(request,"Unauthorized request!")
                return redirect("users:seller_pf")
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")
    def post(self,request,market_id):
        user = CustomUser.objects.get(user=request.user)
        market = get_object_or_404(Market,id=market_id)
        if Seller.objects.filter(user=user):
            seller = Seller.objects.get(user=user)
            if market in seller.supervisor.all():
                form = MarketForm(request.POST)
                if form.is_valid():
                    form = form.cleaned_data
                    market = Market.objects.filter(id=market_id)
                    market.update(
                        name=form.get("name"),
                        desc=form.get("desc"),
                        address=form.get("address"),
                        phone_number=form.get("phone_number"),
                        is_active=form.get("is_active")
                    )
                    messages.success(request,"Market edited successfully!")
                    return redirect("users:seller_pf")
                else:
                    form = MarketForm(request.POST)
                    return render(request,'markets/marketModification.html',{'form':form})

            else:
                messages.error(request,"Unauthorized request!")
                return redirect("users:seller_pf")
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")

class MarketDeletion(LoginRequiredMixin,views.View):
    def get(self,request,market_id):
        user = CustomUser.objects.get(user=request.user)
        market = get_object_or_404(Market,id=market_id)
        if Seller.objects.filter(user=user):
            seller = Seller.objects.get(user=user)
            
            if market in seller.supervisor.all():
                return render(request,"markets/marketDeletion.html",{'market':market})
            else:
                messages.error(request,"Unauthorized request!")
                return redirect("users:seller_pf")
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")
    def post(self,request,market_id):
        user = CustomUser.objects.get(user=request.user)
        market = get_object_or_404(Market,id=market_id)
        if Seller.objects.filter(user=user):
            seller = Seller.objects.get(user=user)
            if market in seller.supervisor.all():
                if request.POST.get("validation") :
                    market = Market.objects.filter(id=market_id).delete()
                    messages.success(request,"Market has been successfully deleted!")
                    return redirect("users:seller_pf")
                else:
                    return redirect("users:seller_pf")
            else:
                messages.error(request,"Unauthorized request!")
                return redirect("users:seller_pf")
        else:
            messages.error(request,"Unauthorized request!")
            return redirect("main")