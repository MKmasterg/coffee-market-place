from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import CustomUser,Seller,Market
from ..forms import RoleMarket

class SellerMainPage(LoginRequiredMixin,View):
    def get(self,request):
        user = CustomUser.objects.get(user=request.user)
        if Seller.objects.filter(user=user).exists():
            seller = Seller.objects.get(user=user)
            return render(request,"users/sellerMainPage.html",{"seller":seller})
        else:
            messages.error(request,"You're unauthorized to view this page!")
            return redirect("main")
        
class SellerAssignment(LoginRequiredMixin,View):
    def get(self,request,market_id):
        Supuser = CustomUser.objects.get(user=request.user)
        if Seller.objects.filter(user=Supuser).exists():
            temp_seller = Seller.objects.get(user=Supuser)
            markets_supervisor = temp_seller.markets.all()
            target_market = get_object_or_404(Market,id=market_id)
            if target_market in markets_supervisor :
                form = RoleMarket.SellerAssignmentForm()
                return render(request,"users/sellerAssignment.html",{"form":form})
            else:
                messages.error(request,"Unauthorized request!")
                return redirect("users:seller_pf")
        else:
            messages.error(request,"You're unauthorized to view this page!")
            return redirect("main")
    def post(self,request,market_id):
        Supuser = CustomUser.objects.get(user=request.user)
        if Seller.objects.filter(user=Supuser).exists():
            temp_seller = Seller.objects.get(user=Supuser)
            markets_supervisor = temp_seller.markets.all()
            target_market = get_object_or_404(Market,id=market_id)
            if target_market in markets_supervisor :
                form = RoleMarket.SellerAssignmentForm(request.POST)
                if form.is_valid():
                    form = form.cleaned_data
                    if User.objects.filter(username=form.get("seller_username")).exists():
                        base_user = User.objects.get(username=form.get("seller_username"))
                        base_user = CustomUser.objects.get(user=base_user)
                        if Seller.objects.filter(user=base_user).exists():
                            target_seller = Seller.objects.get(user=base_user)
                            if target_market not in target_seller.markets.all():
                                target_seller.markets.add(target_market)
                                messages.success(request,"The seller added to you're market's team succefully!")
                                return redirect("users:seller_pf")
                            else:
                                messages.info(request,"The seller is already in you're market's team!")
                                return redirect("users:seller_pf")
                        else:
                            messages.error(request,"User is not a seller!")
                            return render(request,"users/sellerAssignment.html",{"form":RoleMarket.SellerAssignmentForm(request.POST)})    
                    else:
                        messages.error(request,"User not found!")
                        return render(request,"users/sellerAssignment.html",{"form":RoleMarket.SellerAssignmentForm(request.POST)})
                else:
                    messages.error(request,"Something went wrong!")
                    return render(request,"users/sellerAssignment.html",{"form":form})
            else:
                messages.error(request,"Unauthorized request!")
                return redirect("users:seller_pf")
        else:
            messages.error(request,"You're unauthorized to view this page!")
            return redirect("main")
        
class SellerDischarging(LoginRequiredMixin,View):
    def get(self,request,seller_id,market_id):
        supervisor = get_object_or_404(Seller,user=CustomUser.objects.get(user=request.user))
        market = get_object_or_404(Market,id=market_id)
        assigned = get_object_or_404(Seller,id=seller_id)
        if supervisor == assigned:
            messages.error(request,"You can't dischrage yourself!")
            return redirect("users:seller_pf")
        
        if market in supervisor.supervisor.all() and assigned in market.markets_seller_set.all():
            market.markets_seller_set.remove(assigned)
            messages.success(request,f"Seller discharged of {market.name} successfully!")
            return redirect("users:seller_pf")
        else:
            messages.error(request,"Something went wrong!")
            return redirect("main")