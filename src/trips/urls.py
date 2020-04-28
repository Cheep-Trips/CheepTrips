from django.urls import path

from . import views

app_name = 'trips'
urlpatterns = [
    path('', views.start, name='index'),
    path('start', views.start, name='start'),
    path('dest', views.dest, name='dest'),
]