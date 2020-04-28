from django.contrib import admin
from django.urls import include, path

from posts.views import post_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trips/', include('trips.urls')),
]
