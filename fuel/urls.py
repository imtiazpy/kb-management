from django.urls import path
from .views import Dashboard, FuelListView, FuelCreateUpdateView, FuelDetailView, fuel_delete_view
from core.views import StockListView, StockCreateUpdateView, StockDetailView, stock_delete_view, InventoryView, SalesListView, SalesCreateUpdateView

urlpatterns = [
  path('', Dashboard.as_view(), name='fuel_dashboard'),

  path('fuels/', FuelListView.as_view(), name='fuel_list'),
  path('fuels/manage/', FuelCreateUpdateView.as_view(), name='manage_fuel'),
  path('fuels/manage/<int:pk>/', FuelCreateUpdateView.as_view(), name='manage_fuel_edit'),
  path('fuels/save/', FuelCreateUpdateView.as_view(), name='save_fuel'),
  path('fuels/detail/<int:pk>/', FuelDetailView.as_view(), name='fuel_detail'),
  path('fuels/delete/<int:pk>/', fuel_delete_view, name='delete_fuel'),

  path('stocks/fuel/', StockListView.as_view(), {'category': 'FUEL'}, name='fuel_stock'),
  path('stocks/<category>/manage/', StockCreateUpdateView.as_view(), name='manage_stock'),
  path('stocks/manage/<int:pk>/', StockCreateUpdateView.as_view(), {'category': 'FUEL'}, name='manage_stock_edit'),
  path('stocks/save/', StockCreateUpdateView.as_view(), name='save_stock'),
  path('stocks/detail/<int:pk>/', StockDetailView.as_view(), name='stock_detail'),
  path('stocks/delete/<int:pk>/', stock_delete_view, name='delete_stock'),

  path('inventory/<str:category>/', InventoryView.as_view(), name='inventory'),

  path('sales/fuel/', SalesListView.as_view(), {'category': 'FUEL'}, name='sales'),
  path('sales/manage/<category>/', SalesCreateUpdateView.as_view(), name='manage_sale'),
  path('sales/manage/<int:pk>/', SalesCreateUpdateView.as_view(), {'category': 'FUEL'}, name='manage_sale_edit'),
  path('sales/save/', SalesCreateUpdateView.as_view(), name='save_sale'),
  
]