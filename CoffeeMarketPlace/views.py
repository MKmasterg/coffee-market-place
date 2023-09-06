from django.views import View
from django.shortcuts import render
from users.models import Market


class MainPage(View):
    def get(self,request):
        markets = Market.objects.all() if Market.objects.all() else None
        return render(request,"main.html/",{"markets":markets})