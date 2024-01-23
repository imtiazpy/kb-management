from django.urls import path
from .views import FisheriesDashboard, FishListView, FryListView, FishCreateUpdateView, FryCreateUpdateView, FishFryDetailView, fish_fry_delete_view

from core.views import StockListView, StockCreateUpdateView, SalesListView, SalesCreateUpdateView, SalesReportView, SalesReportAdminView

urlpatterns = [
  path('fish-dash/', FisheriesDashboard.as_view(), {'category': 'FISH'}, name='fish_dashboard'),
  path('fry-dash/', FisheriesDashboard.as_view(), {'category': 'FRY'}, name='fry_dashboard'),

  path('fish-dash/fishes/', FishListView.as_view(), name='fish_list'),
  path('fish-dash/fishes/manage/', FishCreateUpdateView.as_view(), name='manage_fish'),
  path('fish-dash/fishes/manage/<int:pk>/', FishCreateUpdateView.as_view(), name='manage_fish_edit'),
  path('fish-dash/fishes/save/', FishCreateUpdateView.as_view(), name='save_fish'),
  path('fish-fry/detail/<int:pk>/', FishFryDetailView.as_view(), name='fish_fry_detail'),
  path('fish-fry/delete/<int:pk>/', fish_fry_delete_view, name='fish_fry_delete'),
  path('fish-dash/stocks/fish/', StockListView.as_view(), {'category': 'FISH'}, name='fish_stock'),
  path('fish-dash/stocks/manage/fish/', StockCreateUpdateView.as_view(), {'category': 'FISH'}, name='manage_fish_stock'),
  path('fish-dash/sales/fish/', SalesListView.as_view(), {'category': 'FISH'}, name='fish_sales'),
  path('fish-dash/sales/manage/fish/', SalesCreateUpdateView.as_view(), {'category': 'FISH'}, name='manage_fish_sale'),
  path('fish-dash/sales/manage/fish/<int:pk>/', SalesCreateUpdateView.as_view(), {'category': 'FISH'}, name='fish_sale_edit'),

  path('fish-dash/sales/report/fish/', SalesReportView.as_view(), {'category': 'FISH'}, name='fish_sales_report_page'),
  path('fish-dash/sales/report/fish/<str:report_date>/', SalesReportView.as_view(), {'category': 'FISH'}, name='fish_sales_report'),
  path('fish-dash/sales/admin/report/fish/', SalesReportAdminView.as_view(), {'category': 'FISH'}, name='fish_sales_report_admin'),

  path('fries/', FryListView.as_view(), name='fry_list'),
  path('fries/manage/', FryCreateUpdateView.as_view(), name='manage_fry'),
  path('fries/manage/<int:pk>/', FryCreateUpdateView.as_view(), name='manage_fry_edit'),
  path('fries/save/', FryCreateUpdateView.as_view(), name='save_fry'),
  path('stocks/fry/', StockListView.as_view(), {'category': 'FRY'}, name='fry_stock'),
  path('stocks/manage/fry/', StockCreateUpdateView.as_view(), {'category': 'FRY'}, name='manage_fry_stock'),
  path('sales/fry/', SalesListView.as_view(), {'category': 'FRY'}, name='fry_sales'),
  path('sales/manage/fry/', SalesCreateUpdateView.as_view(), {'category': 'FRY'}, name='manage_fry_sale'),
  path('sales/manage/fry/<int:pk>/', SalesCreateUpdateView.as_view(), {'category': 'FRY'}, name='fry_sale_edit'),

  path('sales/report/fry/', SalesReportView.as_view(), {'category': 'FRY'}, name='fry_sales_report_page'),
  path('sales/report/fry/<str:report_date>/', SalesReportView.as_view(), {'category': 'FRY'}, name='fry_sales_report'),
  path('sales/admin/report/fry/', SalesReportAdminView.as_view(), {'category': 'FRY'}, name='fry_sales_report_admin'),
]