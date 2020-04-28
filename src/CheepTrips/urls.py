from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('users/', include('users.urls')), 
    # path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', include('trips.urls'))
]
