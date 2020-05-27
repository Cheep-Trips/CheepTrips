from django.contrib import admin
from django.urls import include, path
from .trips.views import RegistrationView

urlpatterns = [
    # path('users/', include('users.urls')), 
    # path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    
    path('accounts/register/',
        RegistrationView.as_view(),
        name='django_registration_register',
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('trips.urls'))
]
