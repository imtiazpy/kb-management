from django.urls import path

from .views import login_page_view, login_view, logout_view

urlpatterns = [
  path('login/', login_page_view, name='login'),
  path('login-user/', login_view, name='login_user'),
  path('logout/', logout_view, name='logout'),
]