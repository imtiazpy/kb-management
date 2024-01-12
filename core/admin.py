from django.contrib import admin

from .models import Product, Customer, Stock, Sale


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Stock)
admin.site.register(Sale)

