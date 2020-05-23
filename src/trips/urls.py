from django.urls import path

from . import views

app_name = 'trips'
urlpatterns = [
    path('', views.WelcomeView.as_view(), name='index'),
    path('welcome', views.WelcomeView.as_view(), name='welcome'),
    path('destination', views.DestinationView.as_view(), name='destination'),
    path('sign_in/', views.SignInView.as_view(), name='sign_in'),
    path('saved_trips/', views.saved_trips, name='saved_trips'),
    path('view_trip/', views.view_trip, name='view_trip'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('compare/', views.compare, name='compare'),
    path('new_account/', views.NewAccountView.as_view(), name='new_account'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('view_flight/', views.ViewFlightView.as_view(), name='view_flight'),
]