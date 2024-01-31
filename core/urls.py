from django.urls import path

from .views import CustomerCreatePageView, ManagementView, AdminManagerView, StaffListView, StaffCreateUpdateView, SalaryCreatePageView, StaffDetailView, staff_delete_view

urlpatterns = [
  path('customer/', CustomerCreatePageView.as_view(), name='customer_page'),
  path('customer/create/', CustomerCreatePageView.as_view(), name='customer_create'),
  path('management/', ManagementView.as_view(), name='management'),
  path('admin/manager/', AdminManagerView.as_view(), name='admin_manager'),
  path('salary/', SalaryCreatePageView.as_view(), name='salary_page'),
  path('salary/create/', SalaryCreatePageView.as_view(), name='salary_create'),
  path('staffs/', StaffListView.as_view(), name="staffs"),
  path('staffs/manage/', StaffCreateUpdateView.as_view(), name='manage_staff'),
  path('staffs/manage/<int:pk>/', StaffCreateUpdateView.as_view(), name="manage_staff_edit"),
  path('staffs/save/', StaffCreateUpdateView.as_view(), name="save_staff"),
  path('staffs/detail/<int:pk>/', StaffDetailView.as_view(), name='staff_detail'),
  path('staffs/delete/<int:pk>/', staff_delete_view, name='delete_staff')
]