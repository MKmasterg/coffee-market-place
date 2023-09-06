from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout,authenticate,login

class LoginView(View):
    def get(self,request):
        form = AuthenticationForm()
        return render(request,'users/login.html',{'form':form})
    def post(self,request):
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.GET :
                    return redirect(request.GET['next'])
                else:
                    return redirect("main")
            else:
                # messages.error(request,"Invalid username or password.")
                error = "Invalid username or password."
                return render(request,'users/login.html',{"form":form,'error':error})
        else:
            error = 'Invalid username or password.'
            return render(request,'users/login.html',{"form":form,'error':error})

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("main")
