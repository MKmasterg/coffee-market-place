from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from ..forms import SignUpSignIn, RoleMarket,UpdateContact
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login , update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import CustomUser,Customer,Seller
import datetime


class SignupView(View):
    def get(self,request):
        form = SignUpSignIn.SignUpForm()
        return render(request,'users/signup.html',{"form":form})
    def post(self,request):
        form = SignUpSignIn.SignUpForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user = User.objects.create_user(
                username=form.get('username'),
                email=form.get('email'),
                password=form.get('password1'),
                first_name=form.get('first_name'),
                last_name=form.get('last_name'),
            )
            CustomUser.objects.create(
                user=user,
                phone_number=form.get('phone_number'),
                id_number=form.get('id_number'),
                date_joined = datetime.datetime.now()
            )
            login(request,user)
            if form.get("role_selector") == 1:
                return redirect("users:customer_sign_up")
            elif form.get("role_selector") == 2:
                return redirect('users:seller_sign_up')
            else:
                return render(request,'users/signup.html',{"form":form})
        else:
            form = SignUpSignIn.SignUpForm(request.POST)
            return render(request,'users/signup.html',{"form":form})

class SellerSignUpView(LoginRequiredMixin,View):
    def get(self,request):
        seller = Seller(user=CustomUser.objects.get(user=request.user))
        seller.save()
        messages.success(request,"Seller registration completed!")
        return redirect('main')

class CustomerSignUpView(LoginRequiredMixin,View):
    def get(self,request):
        form = RoleMarket.RoleCustomer()
        return render(request,'users/customerSignUp.html',{"form":form})
    def post(self,request):
        form = RoleMarket.RoleCustomer(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user = CustomUser.objects.get(user=request.user)
            if Seller.objects.filter(user=user):
                error = "You're recognized as seller, you can't be customer using this account!"
                form = RoleMarket.RoleCustomer(request.POST)
                return render(request,'users/roleSelection.html',{"form":form,"error":error})
            Customer.objects.create(
                user= user,
                home_address= form.get("home_address")
            )
            return redirect('main')
        else:
            form = RoleMarket.RoleCustomer(request.POST)
            return render(request,'users/customerSignUp',{"form":form})
        
class ChangePassword(LoginRequiredMixin,View):
    def get(self,request):
        form = PasswordChangeForm(request.user)
        return render(request,'users/changePassword.html',{"form":form})
    def post(self,request):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("main:main")
        else:
            form = PasswordChangeForm(request.user)
            error = "Something went wrong!"
            messages.error(request,error)
            return render(request, 'users/changePassword.html', {'form': form})
        
class UpdateUser(LoginRequiredMixin,View):
    def get(self,request):
        user = CustomUser.objects.get(user=request.user)
        home_address = Customer.objects.get(user=user).home_address if Customer.objects.filter(user=user) else ""
        payload={
            "phone_number" : user.phone_number,
            "home_address" : home_address
        }

        form = UpdateContact.UpdateUserForm(payload)
        return render(request,"users/updateUser.html",{"form":form})
    def post(self,request):
        user = CustomUser.objects.get(user=request.user)
        form = UpdateContact.UpdateUserForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if Seller.objects.filter(user=user).exists():
                CustomUser.objects.filter(user=request.user).update(
                    phone_number = form.get("phone_number")
                )
                messages.success(request,"User info updated successfully!")
                return redirect("users:seller_pf")
            elif Customer.objects.filter(user=user).exists():
                CustomUser.objects.filter(user=request.user).update(
                    phone_number = form.get("phone_number")
                )
                Customer.objects.filter(user=user).update(
                    home_address = form.get("home_address")
                )
                messages.success(request,"User info updated successfully!")
                return redirect("users:customer_pf")
            else:
                messages.error(request,"IDK what are you doing but you just can't")
                return redirect("main")
        else:
            return render(request,"users/updateUser.html",{"form":form})



