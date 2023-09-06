"""
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from .views import MainPage
# from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls',namespace="users")),
    path('',MainPage.as_view(),name="main"),
    # path('',TemplateView.as_view(template_name='main.html',extra_context={"markets":markets}),name="main"),
    path('markets/',include('markets.urls',namespace="markets")),
]
