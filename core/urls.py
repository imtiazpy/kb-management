from django.urls import path

from .views import CustomerCreatePageView, ManagementView

urlpatterns = [
  path('customer/', CustomerCreatePageView.as_view(), name='customer_page'),
  path('customer/create/', CustomerCreatePageView.as_view(), name='customer_create'),
  path('management/', ManagementView.as_view(), name='management'),
]