from django.contrib import admin
from .models import CustomUser,Customer,Seller,Market,Stock,Order
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False

class CustomizedUserAdmin(UserAdmin):
    inlines = (CustomUserInline,)

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Market)
admin.site.register(Stock)
admin.site.register(Order)