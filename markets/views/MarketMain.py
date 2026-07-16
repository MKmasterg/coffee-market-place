from django.views import View
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib import messages
from users.models import CustomUser , Seller, Market,Customer,Order

class MarketMainPage(View):
    def get(self,request,market_id):
        market = get_object_or_404(Market,id=market_id)
        payload = {
            "market":market,
            "anonymous" : False,
            "supervisor" : False,
            "seller" : False,
            "other_seller" : False,
            "customer" : False,
            "no_role" : False
        }
        # authority level :
        if not request.user.is_authenticated:
            #anonymous
            payload["anonymous"] = True
        else:
            user = CustomUser.objects.get(user=request.user)
            if  Seller.objects.filter(user=user).exists():
                seller = Seller.objects.get(user=user)
                if market in seller.markets.all():
                    #seller of the market
                    payload["seller"] = True
                    if market in seller.supervisor.all():
                        #supervisor of the market
                        payload["supervisor"] = True
                else:
                    #seller but from other markets
                    payload["other_seller"] = True
            elif Customer.objects.filter(user=user).exists():
                #customer
                payload["customer"] = True
            else:
                #neither customer and seller but has a user instance
                payload["no_role"] = True

        if market.is_active and market.is_verified :
            return render(request,"markets/main.html",payload)
        elif payload["supervisor"] :
            return render(request,"markets/main.html",payload)
        else :
            messages.info(request,"Market is currently deactivated!")
            return redirect("main")

    def post(self,request,market_id):
        user = get_object_or_404(CustomUser,user=request.user)
        seller = get_object_or_404(Seller,user=user)
        validator = [300,200,403]
        for key,value in request.POST.dict().items():
            if "status" in key:
                id = int(key[6:])
                if int(value) in validator:
                    Order.objects.filter(id=id).update(status=int(value))
                else:
                    messages.error(request,"Invalid input!")
                    return redirect("markets:market_main",market_id)
        else:
            messages.success(request,"Submitted successfully!")
            return redirect("markets:market_main",market_id)