from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('users/', include('users.urls')),
    path('staff/', include('staffs.urls')),
    path('fuel-dash/', include('fuel.urls')),
]

if settings.DEBUG == True:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
