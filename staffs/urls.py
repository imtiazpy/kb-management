from django.urls import path

from .views import ProfileView, AttendanceCreateView

urlpatterns = [
  path('profile/', ProfileView.as_view(), name='profile'),
  path('profile/update/', ProfileView.as_view(), name='update_profile'),
  path('profile/save/', ProfileView.as_view(), name='save_profile'),
  path('attendance/', AttendanceCreateView.as_view(), name='attendance'),
  path('attendance/sign-in/', AttendanceCreateView.as_view(), name='sign_in'),
]