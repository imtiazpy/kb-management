from django.urls import path
from .views import (
  home_page_view, 
  about_page_view, 
  services_list_page_view, 
  services_detail_page_view,
  teams_page_view,
  contact_page_view,
)
urlpatterns = [
  path('', home_page_view, name='home'),
  path('about/', about_page_view, name='about'),
  path('services/', services_list_page_view, name='services'),
  path('services/<int:pk>/', services_detail_page_view, name='service_detail'),
  path('teams/', teams_page_view, name='teams'),
  path('contact/', contact_page_view, name='contact')
]