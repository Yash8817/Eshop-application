from pathlib import Path
from django.contrib import admin
from django.urls import path
from .views import Index ,  Login , Signup , logout , Cart

urlpatterns = [
    path('', Index.as_view() , name='homepage'),
    path('signup', Signup.as_view()  , name="signup" ) , 
    path('login', Login.as_view() , name="login" ),
    path('logout', logout , name="logout" ),
    path('cart', Cart.as_view() , name="cart" )
]
