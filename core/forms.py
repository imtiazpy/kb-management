from django import forms
from django.contrib.auth import get_user_model
from .models import Product, Stock, Sale, Customer
from staffs.models import Salary, Staff


USER = get_user_model()

class SaveProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'category', 'description',
                  'status', 'price', 'image', 'created_by')

    def clean_name(self):
        name = self.cleaned_data['name']
        id = self.data['id'] if self.data['id'].isdigit() else 0

        if Product.objects.filter(name=name).exclude(id=id).exists():
            raise forms.ValidationError(f"{name} already exists")

        return name

    def clean_price(self):
        price = self.cleaned_data['price']

        if price > 0:
            return price
        raise forms.ValidationError(
            "Invalid price. Please enter a value greater than 0")


class SaveStockForm(forms.ModelForm):

    class Meta:
        model = Stock
        fields = ('product', 'unit', 'volume', 'stock_in', 'created_by')

    def clean_product(self):
        product_id = self.data.get('product')
        try:
            product = Product.objects.get(id=product_id)
            return product
        except Product.DoesNotExist:
            raise forms.ValidationError(
                f"Product with ID {product_id} does not exist.")
        except ValueError:
            raise forms.ValidationError("Invalid Product ID.")

    def clean_volume(self):
        volume = self.cleaned_data['volume']
        if volume > 0:
            return volume
        raise forms.ValidationError(
            "Invalid volume. Please enter a value greater than 0")


class SaveSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('product', 'volume', 'customer', 'price', 'total_amount', 'sale_date', 'created_by')

    def clean_product(self):
        product_id = self.data.get('product')
        try:
            product = Product.objects.get(id=product_id)
            return product
        except Product.DoesNotExist:
            raise forms.ValidationError(f"Product with ID {product_id} does not exist.")
        except ValueError:
            raise forms.ValidationError("Invalid Fuel ID.")

    def clean_volume(self):
        fuel_vol = Product.objects.get(id=self.data.get('product')).available()
        volume = self.data.get('volume')

        if float(volume) <= 0:
            raise forms.ValidationError("Volume must be greater than 0.")
        elif float(volume) <= float(fuel_vol):
            return volume
        else:
            raise forms.ValidationError(
                f"Fuel volume exceeds the limit. Available fuel - {fuel_vol} L")


class SaveCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class SaveSalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = "__all__"


class SaveStaffForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    designation = forms.CharField(max_length=20)
    joining_date = forms.DateField()
    salary = forms.ModelChoiceField(queryset=Salary.objects.all())

    class Meta:
        model = Staff
        fields = ['username', 'password', 'designation', 'joining_date', 'salary']

    
    def save(self, commit=True):
        user, created = USER.objects.get_or_create(username=self.cleaned_data['username'])
        if created:
            user.set_password(self.cleaned_data['password'])
            user.save()
        staff = super().save(commit=False)
        staff.user = user
        staff.designation = self.cleaned_data['designation']
        staff.joining_date = self.cleaned_data['joining_date']
        staff.salary = self.cleaned_data['salary']
        if commit:
            staff.save()
        return staff