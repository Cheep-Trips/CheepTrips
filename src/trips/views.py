import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, RedirectView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django_registration.backends.one_step.views import RegistrationView as BaseRegistrationView
from .forms import NewAccountForm

import requests, json


# from amadeus import Client, ResponseError

from .forms import *
from . import views
from .models import Trip, Flight, Location


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

    def form_invalid(self, form):
        return super().form_invalid(form)

def getSkyscannerCached(departure, departure_date, arrival, inbound_date):
 
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/US/USD/en-US/" + departure + "-sky/" + arrival + "/" + departure_date
 

    querystring = {"inboundpartialdate":inbound_date}
 
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "bad009e854msha1e631baaea5b4cp1f4736jsn72e952c4dfef"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.json())
    response_json = json.loads(response.text)

    places = response_json['Places']
    places_dict = {}
    carriers = response_json['Carriers']
    carriers_dict = {}

    for place in places:
        places_dict[place['PlaceId']] = [place['Name'], place['SkyscannerCode']]
    for carrier in carriers:
        carriers_dict[carrier['CarrierId']] = carrier['Name']
    res={}
    for quote in response_json['Quotes']:
        if(arrival=="Everywhere"): 
            res[places_dict[quote['OutboundLeg']['DestinationId']][0]] = [str(quote['MinPrice']), places_dict[quote['OutboundLeg']['DestinationId']][1]]
        else:
            if(carriers_dict[quote['OutboundLeg']['CarrierIds'][0]] not in res or quote['MinPrice'] < res[carriers_dict[quote['OutboundLeg']['CarrierIds'][0]]]):
                res[carriers_dict[quote['OutboundLeg']['CarrierIds'][0]]] = quote['MinPrice']
    return res

class DestinationView(FormView):
    form_class=DestinationForm
    success_url=reverse_lazy('trips:view_flight')
    destination_url=reverse_lazy('trips:destination')
    template_name='trips/destination.html'

    def get_context_data(self, **kwargs):
        initial = super().get_initial()
        context = super().get_context_data(**kwargs)
        departure = self.request.GET.get('departure', '')
        arrival = self.request.GET.get('arrival', '') if self.request.GET.get('arrival', '') != "" else "Everywhere"
        departure_date = self.request.GET.get('departure_date', '')
        return_date = initial['return_date'] = self.request.GET.get('return_date', '')
        destinations = getSkyscannerCached(departure, departure_date, arrival, return_date)
        context['destinations'] = destinations
        return context

    def get_initial(self):
        initial = super().get_initial()
        departure = initial['departure'] = self.request.GET.get('departure', '')
        initial['arrival'] = self.request.GET.get('arrival', '')
        arrival = initial['arrival'] if initial['arrival'] != "" else "Everywhere"
        departure_date = initial['departure_date'] = self.request.GET.get('departure_date', '')
        return_date = initial['return_date'] = self.request.GET.get('return_date', '')
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

        #skyscanner to cache call here 
        if "with_destination" in form.data and arrival != "":           
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, arrival, departure_date, return_date, price_max, region, activity, travelers, priority)
        elif "without_destination" in form.data:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.destination_url, departure, "", departure_date, return_date, price_max, region, activity, travelers, priority)
        else:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, form.data["set_destination"].split(" - ")[1], departure_date, return_date, price_max, region, activity, travelers, priority)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class ViewFlightView(FormView):
    form_class=DestinationForm
    success_url=reverse_lazy('trips:view_flight')
    destination_url=reverse_lazy('trips:destination')
    template_name='trips/view_flight.html'

    def get_context_data(self, **kwargs):
        initial = super().get_initial()
        context = super().get_context_data(**kwargs)
        departure = self.request.GET.get('departure', '')
        arrival = self.request.GET.get('arrival', '') if self.request.GET.get('arrival', '') != "" else "Everywhere"
        departure_date = self.request.GET.get('departure_date', '')
        return_date = initial['return_date'] = self.request.GET.get('return_date', '')
        destinations = getSkyscannerCached(departure, departure_date, arrival, return_date)
        context['destinations'] = destinations
        context['departure'] = departure
        return context

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

        if "with_destination" in form.data and arrival != "":           
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, arrival, departure_date, return_date, price_max, region, activity, travelers, priority)
        elif "without_destination" in form.data:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&price_max={}&region={}&activity={}&travelers={}&priority={}".format(self.destination_url, departure, "", departure_date, return_date, price_max, region, activity, travelers, priority)
        else:
            #TODO ADD FLIGHT TO TRIP
            pass

        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class ForgotPasswordView(FormView):
    form_class=ForgotPasswordForm
    template_name='trips/forgot_password.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.success_url = reverse_lazy('trips:forgot_password')
        return super().form_valid(form)


class RegistrationView(BaseRegistrationView):
    form_class=NewAccountForm
    success_url=reverse_lazy('trips:welcome')

    def get_form(self, form_class=None):
     data = super().get_form(form_class)
    #  for field in data.fields:
    #     print(dir(field))
     return data

class SignInView(FormView):
    form_class=SignInForm
    template_name='trips/registration/login.html'
    def form_valid(self, form):
        self.success_url = reverse_lazy('trips:welcome')
        return super().form_valid(form)

class ProfileView(FormView):
    form_class=ProfileForm
    template_name='trips/profile.html'
    def form_valid(self, form):
        self.success_url = reverse_lazy('trips:welcome')
        return super().form_valid(form)


class AddFlightView(LoginRequiredMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        carrier = request.POST.get('carrier', None)
        cost = request.POST.get('cost', None)
        departure_name = request.POST.get('departure', None)
        destination_name = request.POST.get('destination', None)
        departure_time = request.POST.get('departure_time', None)
        arrival_time = request.POST.get('arrival_time', None)

        departure = Location.objects.filter(airport=departure_name).first()
        destination = Location.objects.filter(airport=destination_name).first()

        trips = Trip.objects.filter(user=request.user)
        if not trips.count() == 0:
            trip = trips.last()
        else:
            trip = Trip(user=request.user)
            trip.save()
        flight = Flight(
            flight_carrier=carrier,
            departure_location=departure,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            price=int(cost.split('.')[0]),
            trip=trip
        )
        flight.save()

        print(carrier, cost, departure, destination, departure_time, arrival_time)
        self.url = reverse_lazy('trips:saved_trips')
        return super().post(request, *args, **kwargs)

class SavedTripsView(LoginRequiredMixin, TemplateView):
    template_name = 'trips/saved_trips.html'


def saved_trips(request):
    return render(request, 'trips/saved_trips.html', {})
def view_trip(request):
    return render(request, 'trips/view_trip.html', {})
def profile(request):
    return render(request, 'trips/profile.html', {})
def compare(request):
    return render(request, 'trips/compare.html', {})

def view_flight(request):
    return render(request, 'views.ViewFlight.as_view()', {})

def getEchangeRate(request):
    url = 'https://open.exchangerate-api.com/v6/latest/USD'

    # Here is all the exchange rates to all countries from USD
    response = requests.get(url)
    data = response.json()

    return data

def getBudget(request, city):
    #todo (most likely over the weekend)

    url = "https://www.budgetyourtrip.com/api/v3/search/locationdata/" + city
    response = requests.post( url, headers=headers, auth=("apikey", BUDGET_YOUR_TRIP_API_KEY))
