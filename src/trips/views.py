import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy


# from amadeus import Client, ResponseError

from .forms import *
from . import views


class WelcomeView(FormView):
    form_class=WelcomeForm
    success_url=reverse_lazy('trips:view_flight')
    destination_url=reverse_lazy('trips:destination')
    template_name='trips/welcome.html'

    def form_valid(self, form):
        departure = form.cleaned_data['departure']
        departure_date = form.cleaned_data['departure_date']
        return_date = form.cleaned_data['return_date']
        if "with_destination" in form.data:           
           self.success_url = "{}?departure={}&departure_date={}&return_date={}".format(self.success_url, departure, departure_date, return_date)
        else:
           self.success_url = "{}?departure={}&departure_date={}&return_date={}".format(self.destination_url, departure, departure_date, return_date)
        return super().form_valid(form)

class DestinationView(FormView):
    form_class=DestinationForm
    success_url=reverse_lazy('trips:view_flight')
    destination_url=reverse_lazy('trips:destination')
    template_name='trips/destination.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['departure'] = self.request.GET.get('departure', '')
        initial['arrival'] = self.request.GET.get('arrival', '')
        initial['departure_date'] = self.request.GET.get('departure_date', '')
        initial['return_date'] = self.request.GET.get('return_date', '')
        initial['price_max'] = self.request.GET.get('price_max', '1000')
        initial['region'] = self.request.GET.get('region', 'All Regions')
        initial['activity'] = self.request.GET.get('activity', 'All Activities')
        initial['travelers'] = self.request.GET.get('travelers', '1')
        initial['priority'] = self.request.GET.get('priority', 'Prioritize Cheapest Flights')
        return initial


    def form_valid(self, form):
        departure = form.cleaned_data['departure']
        arrival = form.cleaned_data['arrival']
        departure_date = form.cleaned_data['departure_date']
        return_date = form.cleaned_data['return_date']
        price_max = form.cleaned_data['price_max']
        region = form.cleaned_data['region']
        activity = form.cleaned_data['activity']
        travelers = form.cleaned_data['travelers']
        priority = form.cleaned_data['priority']
        if "with_destination" in form.data:           
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, arrival, departure_date, return_date, price_max, region, activity, travelers, priority)
        else:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.destination_url, departure, arrival, departure_date, return_date, price_max, region, activity, travelers, priority)
        return super().form_valid(form)

class ViewFlightView(FormView):
    form_class=DestinationForm
    success_url=reverse_lazy('trips:view_flight')
    destination_url=reverse_lazy('trips:destination')
    template_name='trips/view_flight.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['departure'] = self.request.GET.get('departure', '')
        initial['arrival'] = self.request.GET.get('arrival', '')
        initial['departure_date'] = self.request.GET.get('departure_date', '')
        initial['return_date'] = self.request.GET.get('return_date', '')
        initial['price_max'] = self.request.GET.get('price_max', '1000')
        initial['region'] = self.request.GET.get('region', 'All Regions')
        initial['activity'] = self.request.GET.get('activity', 'All Activities')
        initial['travelers'] = self.request.GET.get('travelers', '1')
        initial['priority'] = self.request.GET.get('priority', 'Prioritize Cheapest Flights')
        return initial

    def form_valid(self, form):
        departure = form.cleaned_data['departure']
        arrival = form.cleaned_data['arrival']
        departure_date = form.cleaned_data['departure_date']
        return_date = form.cleaned_data['return_date']
        price_max = form.cleaned_data['price_max']
        region = form.cleaned_data['region']
        activity = form.cleaned_data['activity']
        travelers = form.cleaned_data['travelers']
        priority = form.cleaned_data['priority']
        if "with_destination" in form.data:           
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, arrival, departure_date, return_date, price_max, region, activity, travelers, priority)
        else:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.destination_url, departure, arrival, departure_date, return_date, price_max, region, activity, travelers, priority)
        return super().form_valid(form)

class ForgotPasswordView(FormView):
    form_class=ForgotPasswordForm
    template_name='trips/forgot_password.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.success_url = reverse_lazy('trips:forgot_password')
        return super().form_valid(form)

class NewAccountView(FormView):
    form_class=NewAccountForm
    template_name='trips/new_account.html'
    def form_valid(self, form):
        self.success_url = reverse_lazy('trips:new_account')
        return super().form_valid(form)

class SignInView(FormView):
    form_class=SignInForm
    template_name='trips/sign_in.html'
    def form_valid(self, form):
        self.success_url = reverse_lazy('trips:welcome')
        return super().form_valid(form)

def sign_in(request):
    return render(request, 'trips/sign_in.html', {})
def saved_trips(request):
    return render(request, 'trips/saved_trips.html', {})
def view_trip(request):
    return render(request, 'trips/view_trip.html', {})
def profile(request):
    return render(request, 'trips/profile.html', {})
def compare(request):
    return render(request, 'trips/compare.html', {})
def new_account(request):
    return render(request, 'trips/new_account.html', {})

def view_flight(request):
    return render(request, 'views.ViewFlight.as_view()', {})
