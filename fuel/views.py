from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.contrib import messages

from core.models import Product, Sale, Stock
from core.forms import SaveProductForm


class Dashboard(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        fuels = Product.objects.filter(category='FUEL', status=1)
        try:
            total_sale = Sale.objects.filter(product__id__in=fuels).aggregate(
                Sum('total_amount'))['total_amount__sum']
            if total_sale is None:
                total_sale = 0
        except:
            total_sale = 0

        context = {
            'total_fuel_count': fuels.count(),
            'fuels': fuels,
            'total_sale': total_sale,
        }

        return render(request, 'fuels/dashboard.html', context)


class FuelListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'fuels/fuel_list.html'
    context_object_name = 'fuels'
    queryset = Product.objects.filter(category='FUEL')


class FuelCreateUpdateView(LoginRequiredMixin, generic.View):
    template_name = 'fuels/manage_fuel.html'
    form_class = SaveProductForm

    def get(self, request, pk=None):
        context = {}
        if pk is not None:
            context['fuel'] = Product.objects.get(id=pk)

        if request.user.is_authenticated:
            context['user'] = request.user.id

        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        res = {'status': 'failed', 'msg': ''}

        if not request.method == 'POST':
            res['msg'] = "No Data was sent"
        else:
            post = request.POST
            if post['id'] != '':
                fuel = Product.objects.get(id=post['id'])
                form = SaveProductForm(request.POST, instance=fuel)
            else:
                form_data = request.POST.copy()
                form_data['category'] = 'FUEL'
                form = SaveProductForm(form_data)

            if form.is_valid():
                form.save()
                if post['id'] == '':
                    messages.success(
                        request, "Fuel has been added successfully")
                else:
                    messages.success(
                        request, "Fuel has been updated successfully")

                res['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not res['msg'] == '':
                            res['msg'] += str('<br />')
                        res['msg'] += str(f"[{field.label}] {error}")

        return JsonResponse(res)


class FuelDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    template_name = 'fuels/fuel_detail.html'
    context_object_name = 'fuel'
    pk_url_kwarg = 'pk'


@login_required
def fuel_delete_view(request, pk=None):
    res = {'status': '', 'msg': ''}

    if pk is None:
        res['msg'] = "Invalid Fuel ID"

    else:
        fuel_instance = get_object_or_404(Product, pk=pk)
        try:
            fuel_instance.delete()
            res['status'] = 'success'
            messages.success(request, "Fuel has been deleted successfully")
        except Exception as e:
            res['msg'] = f"Error deleting Fuel: {str(e)}"

    return JsonResponse(res)

