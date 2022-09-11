from math import prod
from unicodedata import category
from django.contrib import admin
from . models import Product , Category , Customer

# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['First_name','last_name','phone','email']


admin.site.register(Product , AdminProduct)
admin.site.register(Category , AdminCategory)
admin.site.register(Customer , CustomerAdmin)