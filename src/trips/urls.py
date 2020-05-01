from django.urls import path

from . import views

app_name = 'trips'
urlpatterns = [
    path('', views.start, name='index'),
    path('start', views.start, name='start'),
    path('dest', views.dest, name='dest'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('saved_trips/', views.saved_trips, name='saved_trips'),
    path('view_trip/', views.view_trip, name='view_trip'),
]