from django.views import View
from users.models import Market
from django.shortcuts import render

class SearchMarkets(View):
    def get(self,request):
        markets = Market.objects.all() if Market.objects.all() else None
        return render(request,"markets/index.html/",{"markets":markets})
    def post(self,request):
        keyword = request.POST.get("keyword")
        markets = list(Market.objects.filter(name__icontains=keyword)) if Market.objects.filter(name__icontains=keyword).exists() else []
        if Market.objects.filter(desc__icontains=keyword) not in markets:
            markets += list(Market.objects.filter(desc__icontains=keyword)) if Market.objects.filter(desc__icontains=keyword).exists() else []
            markets = list(set(markets))
        return render(request,"markets/index.html/",{"markets":markets})
