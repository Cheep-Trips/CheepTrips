from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.sign_in, name='index'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('saved_trips/', views.saved_trips, name='saved_trips'),
    path('view_trip/', views.view_trip, name='view_trip'),
]