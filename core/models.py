from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

USER = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=(('FUEL', 'Fuel'), ('FISH', 'Fish'), ('FRY', 'Fry')), default=1)
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('0', 'Inactive')), default=1)
    price = models.FloatField(max_length=(15, 2), default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name='user_products')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name}-{self.category}"

    def available(self):
        try:
            stock_in = self.stocks.aggregate(
                models.Sum("volume"))['volume__sum']
            if stock_in is None:
                stock_in = 0
        except:
            stock_in = 0
        try:
            sale = self.sales.aggregate(models.Sum("volume"))['volume__sum']
            if sale is None:
                sale = 0
        except:
            sale = 0
        return stock_in - sale
    

class Customer(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    location = models.CharField(_("Location"), max_length=100, blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=11, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"



class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='stocks')
    unit = models.CharField(max_length=50, choices=(('KG', 'Kg'), ('LITRE', 'Litre')), default='KG')
    volume = models.FloatField(max_length=(15, 2), default=0)
    stock_in = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name='user_stocks')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.product.name}-[{self.volume} L]"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='sales')
    volume = models.FloatField(max_length=(15, 2), default=0)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='customer_sales')
    # price = models.FloatField(max_length=(15, 2), default=0)
    total_amount = models.FloatField(max_length=(15, 2), default=0)
    sale_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name='user_sales')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales"

    def __str__(self):
        return f"{self.customer_name}-[{self.product}-{self.volume} L]"
