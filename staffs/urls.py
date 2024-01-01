from django.urls import path

from .views import ProfileView

urlpatterns = [
  path('profile/', ProfileView.as_view(), name='profile'),
  path('profile/update/', ProfileView.as_view(), name='update_profile'),
  path('profile/save/', ProfileView.as_view(), name='save_profile'),
]