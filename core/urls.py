from django.urls import path

from .views import CustomerCreatePageView, ManagementView, AdminManagerView, StaffListView

urlpatterns = [
  path('customer/', CustomerCreatePageView.as_view(), name='customer_page'),
  path('customer/create/', CustomerCreatePageView.as_view(), name='customer_create'),
  path('management/', ManagementView.as_view(), name='management'),
  path('admin/manager/', AdminManagerView.as_view(), name='admin_manager'),
  path('staffs/', StaffListView.as_view(), name="staffs"),
]