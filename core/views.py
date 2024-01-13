from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Stock, Product, Sale, Customer
from core.forms import SaveStockForm, SaveSaleForm


class StockListView(LoginRequiredMixin, generic.ListView):
    """Stock list view for all the product category"""
    model = Stock
    template_name = 'core/stock_list.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        category = self.kwargs.get('category', '')
        return Stock.objects.filter(product__category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category', '')
        return context


category_to_unit = {
    'FUEL': 'LITRE',
    'FISH': 'KG',
    'FRY': 'KG'
}


class StockCreateUpdateView(LoginRequiredMixin, generic.View):
    """Stock create and edit modal renderer"""
    template_name = 'core/manage_stock.html'
    form_class = SaveStockForm

    def get(self, request, pk=None, category=None):
        context = {}
        if pk is not None:
            context['stock'] = Stock.objects.get(id=pk)
        if category is not None:
            context['products'] = Product.objects.filter(
                category=category, status=1)
            context['product_type'] = category
            context['unit'] = category_to_unit[category]

        if request.user.is_authenticated:
            context['user'] = request.user.id
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        res = {'status': 'failed', 'msg': ''}
        if not request.method == 'POST':
            res['msg'] = "No data send on this request"
        else:
            post = request.POST
            if post['id'] != '':
                stock = Stock.objects.get(id=post['id'])
                form = SaveStockForm(request.POST, instance=stock)
            else:
                form = SaveStockForm(request.POST)
            if form.is_valid():
                form.save()
                if post['id'] == '':
                    messages.success(
                        request, "Stock Record has been added successfully")
                else:
                    messages.success(
                        request, "Stock Record has been updated successfully")
                res['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not res['msg'] == '':
                            res['msg'] += str('<br />')
                        res['msg'] += str(f"[{field.label}] {error}")
        return JsonResponse(res)


class StockDetailView(LoginRequiredMixin, generic.DetailView):
    """Stock detail view for all the product category"""
    model = Stock
    template_name = 'core/stock_detail.html'
    context_object_name = 'stock'
    pk_url_kwarg = 'pk'


@login_required
def stock_delete_view(request, pk=None):
    res = {'status': '', 'msg': ''}
    if pk is None:
        res['msg'] = "Invalid Stock ID"

    else:
        stock_instance = get_object_or_404(Stock, pk=pk)
        try:
            stock_instance.delete()
            res['status'] = 'success'
            messages.success(request, "Stock has been deleted successfully")
        except Exception as e:
            res['msg'] = f"Error deleting Stock: {str(e)}"

    return JsonResponse(res)


class InventoryView(LoginRequiredMixin, generic.View):

    def get(self, request, category=None):
        products = Product.objects.filter(category=category, status=1)
        return render(request, 'core/inventory.html', {'products': products})



class SalesListView(LoginRequiredMixin, generic.ListView):
    model = Sale
    template_name = 'core/sales_list.html'
    context_object_name = 'sales'

    def get_queryset(self):
        category = self.kwargs.get('category', '')
        if self.request.user.is_staff:
            return Sale.objects.filter(product__status=1, product__category=category)
        else:
            return Sale.objects.filter(created_by=self.request.user, product__status=1, product__category=category)



class SalesCreateUpdateView(LoginRequiredMixin, generic.View):

    def get(self, request, pk=None, category=None):
        context = {}
        if pk is not None:
            context['sale'] = Sale.objects.get(id=pk)
        context['products'] = Product.objects.filter(status=1, category=category)
        context['customers'] = Customer.objects.all()
        context['user'] = request.user.id

        return render(request, 'core/manage_sale.html', context)

    def post(self, request):
        res = {'status': 'failed', 'msg': ''}

        if request.method != 'POST':
            res['msg'] = 'No data send on this request'
        
        else:
            post = request.POST

            if post['id'] != '':
                sale = Sale.objects.get(id = post['id'])
                form = SaveSaleForm(request.POST, instance=sale)
            else:
                form = SaveSaleForm(request.POST)
            
            if form.is_valid():
                form.save()
                if post['id'] == '':
                    messages.success(request, "Sale Record has been added successfully")
                else:
                    messages.success(request, "Sale Record has been updated successfully")
                res['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not res['msg'] == '':
                            res['msg'] += str('<br />')
                        res['msg'] += str(f"[{field.label}] {error}")
        return JsonResponse(res)