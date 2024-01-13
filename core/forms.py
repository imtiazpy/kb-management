from django import forms
from .models import Product, Stock, Sale


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
        fields = ('product', 'volume', 'customer', 'total_amount', 'sale_date', 'created_by')

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
