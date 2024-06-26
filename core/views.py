from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime



from .models import Stock, Product, Sale, Customer
from staffs.models import Staff, Attendance, Salary
from core.forms import SaveStockForm, SaveSaleForm, SaveCustomerForm, SaveSalaryForm, SaveStaffForm


USER = get_user_model()


class AdminManagerView(LoginRequiredMixin, generic.View):
    template_name = "core/admin_manager.html"

    def get(self, request):
        if request.user.is_staff:
            staffs = Staff.objects.all()
            attending_staffs = Attendance.objects.filter(date__date=datetime.now().date())
            fuels = Product.objects.filter(category='FUEL', status=1)
            total_fuel_sale = Sale.objects.filter(product__id__in=fuels).aggregate(
                Sum('total_amount'))['total_amount__sum']
            
            fishes = Product.objects.filter(category='FISH', status=1)
            fries = Product.objects.filter(category='FRY', status=1)
            fishes_total_sale = Sale.objects.filter(product__id__in=fishes).aggregate(Sum('total_amount'))['total_amount__sum']
            fries_total_sale = Sale.objects.filter(product__id__in=fries).aggregate(Sum('total_amount'))['total_amount__sum']

            context = {
                "staffs_count": staffs.count(),
                "attending_count": attending_staffs.count(),
                "fuel_count": fuels.count(),
                "total_fuel_sale": total_fuel_sale,
                "fishes_count": fishes.count(),
                "fries_count": fries.count(),
                "fishes_total_sale": fishes_total_sale,
                "fries_total_sale": fries_total_sale
            }
            return render(request, self.template_name, context)
        else:
            return render(request, "404.html")


class ManagementView(LoginRequiredMixin, generic.View):

    template_name = 'core/management.html'

    def get(self, request):

        return render(request, self.template_name)



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

    def get_template_names(self):
        category = self.kwargs.get('category', '')
        if category == 'FISH':
            return ['fisheries/fish_stock_list.html']
        elif category == 'FRY':
            return ['fisheries/fry_stock_list.html']
        else:
            return super().get_template_names()


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

    def get_template_names(self):
        category = self.kwargs.get('category', '')
        if category == 'FISH':
            return ['fisheries/fish_sale_list.html']
        elif category == 'FRY':
            return ['fisheries/fry_sale_list.html']
        else:
            return super().get_template_names()


class SalesCreateUpdateView(LoginRequiredMixin, generic.View):

    def get(self, request, pk=None, category=None):
        context = {}
        if pk is not None:
            context['sale'] = Sale.objects.get(id=pk)
        context['products'] = Product.objects.filter(status=1, category=category)
        context['customers'] = Customer.objects.all()
        context['user'] = request.user.id
        context['category'] = category
        context['unit'] = category_to_unit[category]

        return render(request, 'core/manage_sale.html', context)

    def post(self, request):
        res = {'status': 'failed', 'msg': ''}

        if request.method != 'POST':
            res['msg'] = 'No data send on this request'
        else:
            post = request.POST
            if post['id'] != '':
                sale = Sale.objects.get(id=post['id'])
                form = SaveSaleForm(request.POST, instance=sale)
            else:
                form = SaveSaleForm(request.POST)

            if form.is_valid():
                form.save()
                if post['id'] == '':
                    messages.success(
                        request, "Sale Record has been added successfully")
                else:
                    messages.success(
                        request, "Sale Record has been updated successfully")
                res['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not res['msg'] == '':
                            res['msg'] += str('<br />')
                        res['msg'] += str(f"[{field.label}] {error}")
        return JsonResponse(res)


class SalesDetailView(LoginRequiredMixin, generic.DetailView):
    """Stock detail view for all the product category"""
    model = Sale
    template_name = 'core/sale_detail.html'
    context_object_name = 'sale'
    pk_url_kwarg = 'pk'


        


@login_required
def sales_delete_view(request, pk=None):
    res = {'status': '', 'msg': ''}
    if pk is None:
        res['msg'] = "Invalid Sale ID"

    else:
        sale_instance = get_object_or_404(Sale, pk=pk)
        try:
            sale_instance.delete()
            res['status'] = 'success'
            messages.success(request, "Sale has been deleted successfully")
        except Exception as e:
            res['msg'] = f"Error deleting Sale: {str(e)}"

    return JsonResponse(res)


class CustomerCreatePageView(LoginRequiredMixin, generic.View):
    template_name = 'core/customer.html'

    def get(self, request):
        form = SaveCustomerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SaveCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales')
        else:
            return render(request, self.template_name, {'form': form})



class SalesReportView(LoginRequiredMixin, generic.View):
    template_name = 'core/sales_report.html'

    def get(self, request, report_date=None, category=None):
        context = {}
        if report_date is not None:
            report_date = datetime.strptime(report_date, "%Y-%m-%d")
        else:
            report_date = datetime.now()
        
        year = report_date.strftime("%Y")
        month = report_date.strftime("%m")
        day = report_date.strftime("%d")

        products = Product.objects.filter(status=1, category=category)
        sales = Sale.objects.filter(created_by = request.user, product__id__in=products, sale_date__month = month, sale_date__day=day, sale_date__year=year)

        context['report_date'] = report_date
        context['sales'] = sales
        context['total_sale'] = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        return render(request, self.template_name, context)
    


def is_staff_user(user):
    return user.is_staff


@method_decorator(user_passes_test(is_staff_user, login_url=None), name='dispatch')
class SalesReportAdminView(LoginRequiredMixin, generic.ListView):
    model = Sale
    template_name = 'core/sales_report_admin.html'
    context_object_name = 'sales'
    queryset = Sale.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_sale = self.get_queryset()
        user = self.request.GET.get('user')
        context['users'] = USER.objects.filter(is_active=True)
        context['selected_date'] = self.request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
        context['total_sale'] = filtered_sale.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        if user:
            context['selected_user'] = int(user) if user.isdigit() else user
            context['selected_user_name'] = USER.objects.get(id = user) if user.isdigit() else 'All'

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('category', '')

        filters = Q(product__id__in=Product.objects.filter(status=1, category=category))

        date = self.request.GET.get('sale_date')
        report_date = timezone.datetime.strptime(date, "%Y-%m-%d") if date else timezone.now()

        user_id = self.request.GET.get('user')
        if user_id and user_id.lower() == 'all':
            pass
        else:
            filters &= Q(created_by=user_id)

        if date:
            filters &= Q(sale_date=report_date)

        if filters:
            queryset = queryset.filter(filters)
        
        return queryset
    
    def get_template_names(self):
        category = self.kwargs.get('category', '')
        if category == 'FISH':
            return ['fisheries/fish_sale_report_admin.html']
        elif category == 'FRY':
            return ['fisheries/fry_sale_report_admin.html']
        else:
            return super().get_template_names()
        

@method_decorator(user_passes_test(is_staff_user, login_url=None), name='dispatch')
class StaffListView(LoginRequiredMixin, generic.ListView):
    model = Staff
    template_name = "core/staff_list.html"
    context_object_name = "staffs"
    queryset = Staff.objects.all()



@method_decorator(user_passes_test(is_staff_user, login_url=None), name='dispatch')
class StaffCreateUpdateView(LoginRequiredMixin, generic.View):
    template_name = "core/manage_staff.html"

    def get(self, request, pk=None):
        context = {}
        if pk is not None:
            context['staff'] = Staff.objects.get(id=pk)
        context['salaries'] = Salary.objects.all()

        if request.user.is_authenticated:
            context['user'] = request.user.id
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        res = {'status': 'failed', 'msg': ''}

        if request.method != 'POST':
            res['msg'] = 'No data send on this request'
        else:
            post = request.POST
            if post['id'] != '':
                staff = Staff.objects.get(id=post['id'])
                form = SaveStaffForm(request.POST, instance=staff)
            else:
                form = SaveStaffForm(request.POST)

            if form.is_valid():
                form.save()
                if post['id'] == '':
                    messages.success(
                        request, "Staff Record has been added successfully")
                else:
                    messages.success(
                        request, "Staff Record has been updated successfully")
                res['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not res['msg'] == '':
                            res['msg'] += str('<br />')
                        res['msg'] += str(f"[{field.label}] {error}")
        return JsonResponse(res)

@method_decorator(user_passes_test(is_staff_user, login_url=None), name='dispatch')
class StaffDetailView(LoginRequiredMixin, generic.DetailView):
    model = Staff
    template_name = 'core/staff_detail.html'
    context_object_name = 'staff'
    pk_url_kwarg = 'pk'


@user_passes_test(is_staff_user, login_url=None)
@login_required
def staff_delete_view(request, pk=None):
    res = {'status': '', 'msg': ''}

    if pk is None:
        res['msg'] = "Invalid Staff ID"

    else:
        staff_instance = get_object_or_404(Staff, pk=pk)
        user_instance = staff_instance.user
        try:
            staff_instance.delete()
            user_instance.delete()
            res['status'] = 'success'
            messages.success(request, "Staff has been deleted successfully")
        except Exception as e:
            res['msg'] = f"Error deleting Staff: {str(e)}"

    return JsonResponse(res)

@method_decorator(user_passes_test(is_staff_user, login_url=None), name='dispatch')
class SalaryCreatePageView(LoginRequiredMixin, generic.View):
    template_name = 'core/salary.html'

    def get(self, request):
        form = SaveSalaryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SaveSalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staffs')
        else:
            return render(request, self.template_name, {'form': form})