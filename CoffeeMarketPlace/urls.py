"""
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include

from django.views import View
from django.shortcuts import render
from users.models import Market

class MainPage(View):
    def get(self,request):
        markets = Market.objects.all() if Market.objects.all() else None
        return render(request,"main.html/",{"markets":markets})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls',namespace="users")),
    path('',MainPage.as_view(),name="main"),
    path('markets/',include('markets.urls',namespace="markets")),
]
