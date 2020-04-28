from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trips/', include('trips.urls')),
    path('', include('users.urls')), 
    path('users/', include('users.urls')),
]
