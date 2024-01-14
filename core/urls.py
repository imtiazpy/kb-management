from django.urls import path

from .views import CustomerCreatePageView

urlpatterns = [
  path('customer/', CustomerCreatePageView.as_view(), name='customer_page'),
  path('customer/create/', CustomerCreatePageView.as_view(), name='customer_create'),
]