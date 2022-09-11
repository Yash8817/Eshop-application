from distutils.log import error
from distutils.sysconfig import customize_compiler
import http
from operator import methodcaller
from unicodedata import category
from wsgiref.validate import validator
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Product , Category , Customer
from django.contrib.auth.hashers import make_password , check_password
from django.views import View



# Create your views here.

class Index(View):
    
    def post(self , request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        
        cart = request.session.get('cart')

        if cart:
            qty = cart.get(product_id)
            if qty:
                if remove:

                    if qty <= 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] -= 1

                else:
                    cart[product_id] += 1
            else:
                cart[product_id] = 1

        else:
            cart = {}
            cart[product_id] = 1
        
        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        cart = request.session.get('cart')

        if not cart:
            request.session['cart'] = {}

        prds = None
        categoryId = request.GET.get('category')
        if categoryId:
            prds = Product.get_all_product_by_category_ID(categoryId)
        else:
            prds = Product.get_all_product()
        
        Categories = Category.get_all_category()
        data = {
            'prds' : prds , 
            'Categories' : Categories
        }
        return render(request , "index.html" , data)

    
    

class Signup(View):

    def get(self , request):
        return render(request , "signup.html")
    
    def post(self , request):
        PostData = request.POST
        fname = PostData.get("fname")
        lname = PostData.get("lname")
        email = PostData.get("email")
        password = PostData.get("password")
        mobile = PostData.get("mobile")

        values = {
            'fname' : fname , 
            'lname' : lname ,
            'email' : email ,
            'password' : password ,
            'mobile' : mobile
        }
        #creating customer model object
        customer = Customer(First_name = fname , last_name = lname , phone = mobile , password = password , email = email)

        # validation
        error_message = self.ValidateCustomer(customer)
        

        #is no error is there then create customer
        if not error_message:         
            #hash password   
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'values' : values , 
                'error':error_message
            }
            return render(request , "signup.html" , data)

    def ValidateCustomer(self , customer):
        error_message = None
        if not customer.First_name:
            error_message = "First name required !"
        elif not customer.last_name:
            error_message = "Last name required !"
        elif not customer.email:
            error_message = "email required !"
        elif len(customer.email) < 4 :
            error_message = "invalid email !"
        elif not customer.password:
            error_message = "password required !"
        elif len(customer.password) < 8 :
            error_message = "password should be grater than 8 character !"
        elif not customer.phone:
            error_message = "mobile required !"
        elif len(customer.phone) < 10 :
            error_message = "invalid mobile !"
        elif customer.isexist():
            error_message = "Email already exist !"

        

class Login(View):
    def get(self , request):
        return render(request , "login.html")
    
    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check if customer exist if there then get the object
        customer = Customer.GetUser(email)

        error_message = None
        if customer:
            #validate password
            flag = check_password(password , customer.password)

            #if password match
            if flag:
                request.session['customer'] = customer.id
                
                return redirect("homepage")
            else:
                error_message = "Email address or passwprd is invalid !"
                return render(request , "login.html" , {'error' : error_message})

        else:
            error_message = "Email not exist !"
            return render(request , "login.html" , {'error' : error_message})


def logout(request):
    request.session.clear()
    return redirect('login')



class Cart(View):
    def get(self , request):
        product_list = list(request.session.get('cart'))
        product_data = Product.get_product_by_id(product_list)
        print(product_data)
        return render(request , "cart.html")
  