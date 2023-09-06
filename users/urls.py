from django.urls import path
from .views import LoginMain,Signup,Markets,SellerControl,CustomerControl

app_name = "users"
urlpatterns = [
    path("login/",LoginMain.LoginView.as_view(),name="login"),
    path("logout/",LoginMain.Logout.as_view(),name="logout"),
    path("signup/",Signup.SignupView.as_view(),name="signup"),
    path("changePassword/",Signup.ChangePassword.as_view(),name="change_password"),
    path("updateUser/",Signup.UpdateUser.as_view(),name="update_user"),
    path("signup/customerSignUp/",Signup.CustomerSignUpView.as_view(),name="customer_sign_up"),
    path("signup/SellerSignUp/",Signup.SellerSignUpView.as_view(),name="seller_sign_up"),
    path("seller/",SellerControl.SellerMainPage.as_view(),name="seller_pf"),
    path("seller/assignment/<int:market_id>/",SellerControl.SellerAssignment.as_view(),name="seller_assignment"),
    path("seller/discharging/<int:seller_id>/<int:market_id>/",SellerControl.SellerDischarging.as_view(),name="seller_discharging"),
    path("createMarket/",Markets.CreateMarket.as_view(),name="create_market"),
    path("customer/",CustomerControl.CustomerMain.as_view(),name="customer_pf"),
    path("customer/addToBasket/<int:stock_id>/",CustomerControl.AddToBasket.as_view(),name="add_to_basket"),
    path("customer/removeFromBasket/<int:stock_id>/",CustomerControl.RemoveFromBasket.as_view(),name="remove_from_basket"),
    path("customer/contactInfo/<int:customer_id>/",CustomerControl.CustomerContactInfo.as_view(),name="cusotmer_contact_ifo"),

]
