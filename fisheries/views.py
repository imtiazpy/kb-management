from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages

from core.models import Product, Sale, Stock
from core.forms import SaveProductForm


class FisheriesDashboard(LoginRequiredMixin, generic.View):
    
    def get(self, request, *args, **kwargs):
        category = kwargs.get('category', '').upper()            

        products = Product.objects.filter(category=category, status=1)

        # fishes = Product.objects.filter(category='FISH', status=1)
        # fries = Product.objects.filter(category='FRY', status=1)

        try:
            products_total_sale = Sale.objects.filter(product__id__in=products)
            
            # fishes_total_sale = Sale.objects.filter(product__id__in=fishes).aggregate(Sum('total_amount'))['total_amount__sum']
            # fries_total_sale = Sale.objects.filter(product__id__in=fries).aggregate(Sum('total_amount'))['total_amount__sum']

            if products_total_sale is None:
                products_total_sale = 0
            
            """
            if fishes_total_sale is None:
                fishes_total_sale = 0
            
            if fries_total_sale is None:
                fries_total_sale = 0
            """
        except:
            products_total_sale = 0
            # fishes_total_sale = 0
            # fries_total_sale = 0
        
        context = {
            'total_product_count': products.count(),
            'products': products,
            'total_product_sale': products_total_sale,
            'category': category
            # 'total_fish_count': fishes.count(),
            # 'total_fry_count': fries.count(),
            # 'fishes': fishes,
            # 'fries': fries,
            # 'total_fish_sale': fishes_total_sale,
            # 'total_fry_sale': fries_total_sale
        }

        return render(request, 'fisheries/dashboard.html', context)


class FishListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'fisheries/fish_list.html'
    context_object_name = 'fishes'
    queryset = Product.objects.filter(category='FISH')


class FryListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'fisheries/fry_list.html'
    context_object_name = 'fries'
    queryset = Product.objects.filter(category='FRY')



class FishCreateUpdateView(LoginRequiredMixin, generic.View):
    template_name = 'fisheries/manage_fish.html'
    form_class = SaveProductForm

    def get(self, request, pk=None, category=None):
        context = {}
        if pk is not None:
            context['product'] = Product.objects.get(id=pk)

        if request.user.is_authenticated:
            context['user'] = request.user.id

        return render(request, self.template_name, context)
    
    def post(self, request):
        res = {'status': 'failed', 'msg': ''}

        if not request.method == 'POST':
            res['msg'] = "No Data was sent"
        else:
            post = request.POST
            if post['id'] != '':
                product = Product.objects.get(id=post['id'])
                form = SaveProductForm(request.POST, instance=product)
            else:
                form_data = request.POST.copy()
                form_data['category'] = 'FISH'
                form = SaveProductForm(form_data)

            if form.is_valid():
                form.save()
                if post['id'] == '':
                    messages.success(
                        request, f"Fish has been added successfully")
                else:
                    messages.success(
                        request, f"Fish has been updated successfully")

                res['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not res['msg'] == '':
                            res['msg'] += str('<br />')
                        res['msg'] += str(f"[{field.label}] {error}")

        return JsonResponse(res)


class FishFryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    template_name = 'fisheries/fish_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'


@login_required
def fish_fry_delete_view(request, pk=None):
    res = {'status': '', 'msg': ''}

    if pk is None:
        res['msg'] = "Invalid ID"

    else:
        product_instance = get_object_or_404(Product, pk=pk)
        try:
            product_instance.delete()
            res['status'] = 'success'
            messages.success(request, f"{product_instance.category} has been deleted successfully")
        except Exception as e:
            res['msg'] = f"Error deleting Fuel: {str(e)}"

    return JsonResponse(res)
    

class FryCreateUpdateView(LoginRequiredMixin, generic.View):
    template_name = 'fisheries/manage_fry.html'
    form_class = SaveProductForm

    def get(self, request, pk=None, category=None):
        context = {}
        if pk is not None:
            context['product'] = Product.objects.get(id=pk)

        if request.user.is_authenticated:
            context['user'] = request.user.id

        return render(request, self.template_name, context)
    
    def post(self, request):
        res = {'status': 'failed', 'msg': ''}

        if not request.method == 'POST':
            res['msg'] = "No Data was sent"
        else:
            post = request.POST
            if post['id'] != '':
                product = Product.objects.get(id=post['id'])
                form = SaveProductForm(request.POST, instance=product)
            else:
                form_data = request.POST.copy()
                form_data['category'] = 'FRY'
                form = SaveProductForm(form_data)

            if form.is_valid():
                form.save()
                if post['id'] == '':
                    messages.success(
                        request, f"Fry has been added successfully")
                else:
                    messages.success(
                        request, f"Fry has been updated successfully")

                res['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not res['msg'] == '':
                            res['msg'] += str('<br />')
                        res['msg'] += str(f"[{field.label}] {error}")

        return JsonResponse(res)