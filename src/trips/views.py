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
from collections import OrderedDict

import datetime


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
        self.success_url = "{}?departure={}&departure_date={}&return_date={}&departure_id={}".format(self.destination_url, departure.airport, departure_date, return_date, departure.id)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

def getSkyscannerCached(departure, departure_date, arrival, inbound_date):
 
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/US/USD/en-US/" + departure + "-sky/" + arrival + "/" + departure_date

    querystring = {"inboundpartialdate":inbound_date}
 
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "d8bd090baamsh2d471b50a2f602dp172bf3jsn6ae1f2747d21"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = response.json()

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
            res[places_dict[quote['OutboundLeg']['DestinationId']][0]] = [quote['MinPrice'], places_dict[quote['OutboundLeg']['DestinationId']][1]]
        else:
            if(carriers_dict[quote['OutboundLeg']['CarrierIds'][0]] not in res or quote['MinPrice'] < res[carriers_dict[quote['OutboundLeg']['CarrierIds'][0]]][0]):
                res[carriers_dict[quote['OutboundLeg']['CarrierIds'][0]]] = [quote['MinPrice'], places_dict[quote['OutboundLeg']['DestinationId']][1]]
    # return res
    return OrderedDict(sorted(res.items(), key=lambda x: x[1]))

class UpdateSearchView(FormView):
    form_class=DestinationForm
    success_url=reverse_lazy('trips:destination')
    destination_url=reverse_lazy('trips:destination')

    def form_valid(self, form):
        departure = form.cleaned_data['departure']
        departure_date = form.cleaned_data['departure_date']
        return_date = form.cleaned_data['return_date']
        arrival = form.cleaned_data['arrival']
        self.success_url = "{}?departure={}&departure_date={}&return_date={}&departure_id={}".format(self.destination_url, departure.airport, departure_date, return_date, departure.id)
        if arrival:
            self.success_url += "&arrival_id={}".format(arrival.id)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return self.form_valid(form)


class DestinationView(FormView):
    form_class=DestinationForm
    success_url=reverse_lazy('trips:view_flight')
    destination_url=reverse_lazy('trips:destination')
    template_name='trips/destination.html'

    def get_context_data(self, **kwargs):
        initial = self.get_initial()
        context = super().get_context_data(**kwargs)
        context['departure'] = initial['departure']
        departure = self.request.GET.get('departure', '')
        arrival = self.request.GET.get('arrival', '') if self.request.GET.get('arrival', '') != "" else "Everywhere"
        departure_date = self.request.GET.get('departure_date', '')
        return_date = initial['return_date'] = self.request.GET.get('return_date', '')
        oldDestinations = getSkyscannerCached(departure, departure_date, arrival, return_date)
        budget = self.request.GET.get('daily_budget', 'value_budget')
        travelers = self.request.GET.get('travelers', 1)
        flight_type = self.request.GET.get('flight_type', '1') #integer (1 or 2) that specifies whether one-way or round-trip
        
        destinations = {}
        for k, v in oldDestinations.items():
            destinations[k] = []
            for x in v:
                destinations[k].append(x)
            if budget == 'value_budget':
                destinations[k].append((hash(v[1]) % 30) + 30)#getBudget(departure.upper(), v[1], budget))
            elif budget == 'value_midrange':
                destinations[k].append((hash(v[1]) % 30) + 100)
            else:
                destinations[k].append((hash(v[1]) % 30) + 200)
            date_format = "%Y-%m-%d"
            a = datetime.datetime.strptime(return_date, date_format)
            b = datetime.datetime.strptime(departure_date, date_format)
            delta = a-b
            destinations[k].append(delta.days)
            destinations[k].append(travelers)
            destinations[k][0] = destinations[k][0] * int(flight_type)
            destinations[k].append(int(travelers) * int((destinations[k][0]) + destinations[k][3] * destinations[k][2]))
       
        context['destinations'] = destinations
        return context

    def get_initial(self):
        initial = super().get_initial()
        departure_id = self.request.GET.get('departure_id', '')
        departure = Location.objects.get(id=departure_id)
        initial['departure'] = departure
        arrival_id = self.request.GET.get('arrival_id', '')
        if arrival_id:
            arrival = Location.objects.get(id=arrival_id)
            initial['arrival'] = arrival
        else:
            initial['arrival'] = ''

        # arrival = initial['arrival'] if initial['arrival'] != "" else "Everywhere"
        departure_date = initial['departure_date'] = self.request.GET.get('departure_date', '')
        return_date = initial['return_date'] = self.request.GET.get('return_date', '')
        initial['daily_budget'] = self.request.GET.get('daily_budget', 'value_budget')
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
        daily_budget = form.cleaned_data['daily_budget']
        region = form.cleaned_data['region']
        activity = form.cleaned_data['activity']
        travelers = form.cleaned_data['travelers']
        priority = form.cleaned_data['priority']

        #skyscanner to cache call here 
        if "with_destination" in form.data and arrival != "":           
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&daily_budget={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, arrival, departure_date, return_date, daily_budget, region, activity, travelers, priority)
        elif "with_destination" in form.data:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&daily_budget={}&region={}&activity={}&travelers={}&priority={}".format(self.destination_url, departure, arrival, departure_date, return_date, daily_budget, region, activity, travelers, priority)
        elif "without_destination" in form.data:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&daily_budget={}&region={}&activity={}&travelers={}&priority={}".format(self.destination_url, departure, "", departure_date, return_date, daily_budget, region, activity, travelers, priority)
        else:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&daily_budget={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, form.data["set_destination"].split(" ")[-1], departure_date, return_date, daily_budget, region, activity, travelers, priority)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class SelectDestinationView(RedirectView):
    url=reverse_lazy('trips:view_flight')

    def post(self, request, *args, **kwargs):
        departure_id = self.request.POST.get('departure_id')
        departure_date = self.request.POST.get('departure_date')
        return_date = self.request.POST.get('return_date')
        arrival = self.request.POST.get('arrival')
        self.url = "{}?departure_date={}&return_date={}&departure_id={}&arrival={}".format(self.url, departure_date, return_date, departure_id, arrival)
        return super().post(request, *args, **kwargs)

class ViewFlightView(FormView):
    form_class=DestinationForm
    success_url=reverse_lazy('trips:view_flight')
    destination_url=reverse_lazy('trips:destination')
    template_name='trips/view_flight.html'
    

    def get_context_data(self, **kwargs):
        initial = super().get_initial()
        context = super().get_context_data(**kwargs)
        departure = self.request.GET.get('departure', 'lax')
        arrival = self.request.GET.get('arrival', '') if self.request.GET.get('arrival', '') != "" else "Everywhere"
        departure_date = self.request.GET.get('departure_date', '')
        return_date = initial['return_date'] = self.request.GET.get('return_date', '')
        oldDestinations = getSkyscannerCached(departure, departure_date, arrival, return_date)
        budget = self.request.GET.get('daily_budget', 'value_budget')
        travelers = self.request.GET.get('travelers', 1)
        flight_type = self.request.GET.get('flight_type', '1') #integer (1 or 2) that specifies whether one-way or round-trip


        destinations = {}
        for k, v in oldDestinations.items():
            destinations[k] = []
            for x in v:
                destinations[k].append(x)
            if budget == 'value_budget':
                destinations[k].append((hash(v[1]) % 30) + 30)#getBudget(departure.upper(), v[1], budget))
            elif budget == 'value_midrange':
                destinations[k].append((hash(v[1]) % 30) + 100)
            else:
                destinations[k].append((hash(v[1]) % 30) + 200)
            date_format = "%Y-%m-%d"
            a = datetime.datetime.strptime(return_date, date_format)
            b = datetime.datetime.strptime(departure_date, date_format)
            delta = a-b
            destinations[k].append(delta.days)
            destinations[k].append(travelers)
            destinations[k][0] = destinations[k][0] * int(flight_type)
            destinations[k].append(int(travelers) * int((destinations[k][0]) + destinations[k][3] * destinations[k][2]))

        context['destinations'] = destinations
        context['departure'] = departure
        return context

    def get_initial(self):
        initial = super().get_initial()
        departure_id = self.request.GET.get('departure_id', '')
        departure = Location.objects.get(id=departure_id)
        initial['departure'] = departure
        arrival_airport = self.request.GET.get('arrival', '')
        if arrival_airport:
            arrival = Location.objects.get(airport=arrival_airport)
            initial['arrival'] = arrival
        else:
            initial['arrival'] = ''
        initial['departure_date'] = self.request.GET.get('departure_date', '')
        initial['return_date'] = self.request.GET.get('return_date', '')
        initial['daily_budget'] = self.request.GET.get('daily_budget', '1000')
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
        daily_budget = form.cleaned_data['daily_budget']
        region = form.cleaned_data['region']
        activity = form.cleaned_data['activity']
        travelers = form.cleaned_data['travelers']
        priority = form.cleaned_data['priority']

        if "with_destination" in form.data and arrival != "":           
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&daily_budget={}&region={}&activity={}&travelers={}&priority={}".format(self.success_url, departure, arrival, departure_date, return_date, daily_budget, region, activity, travelers, priority)
        elif "without_destination" in form.data:
            self.success_url = "{}?departure={}&arrival={}&departure_date={}&return_date={}&daily_budget={}&region={}&activity={}&travelers={}&priority={}".format(self.destination_url, departure, "", departure_date, return_date, daily_budget, region, activity, travelers, priority)
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
        departure_name = request.POST.get('departure', None).upper()
        destination_name = request.POST.get('destination', None).upper()
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
        self.url = reverse_lazy('trips:saved_trips')
        return super().post(request, *args, **kwargs)

class SavedTripsView(LoginRequiredMixin, TemplateView):
    template_name = 'trips/saved_trips.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trips = Trip.objects.filter(user=self.request.user).all()
        context['trips'] = trips
        return context

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

def getExchangeRate(request):
    url = 'https://open.exchangerate-api.com/v6/latest/USD'

    # Here is all the exchange rates to all countries from USD
    response = requests.get(url)
    data = response.json()

    return data

def getBudget(departureAirport, arrivalAirport, choice):
    #todo (most likely over the weekend)
     #getting city names based on airport
 
    departureCityLoc = Location.objects.filter(airport=departureAirport).first()
    departureCity = departureCityLoc.city

    arrivalCityLoc = Location.objects.filter(airport=arrivalAirport).first()
    arrivalCity = arrivalCityLoc.city

    headers = {
        "X-API-KEY": "RIESEWISMERUCSD2020"
    }
    #gets geonameid
    arrivalurl = "https://www.budgetyourtrip.com/api/v3/search/locationdata/" + arrivalCity
    arrivalResponse = requests.request("GET", arrivalurl, headers=headers)
    arrival_response_json = json.loads(arrivalResponse.text)

    geonameid = arrival_response_json['data'][0]['geonameid']
    arrivalCurrency = arrival_response_json['data'][0]['currency_code']

    departureurl = "https://www.budgetyourtrip.com/api/v3/search/locationdata/" + departureCity
    departureResponse = requests.request("GET", departureurl, headers=headers)
    departure_response_json = json.loads(departureResponse.text)

    departureCurrency = departure_response_json['data'][0]['currency_code']

    
    #gets the user chosen budget
    budgeturl = "https://www.budgetyourtrip.com/api/v3/costs/locationinfo/" + geonameid
    budgetResponse = requests.request("GET", budgeturl, headers=headers)
    budget_json = json.loads(budgetResponse.text)
    daily_budget = budget_json['data']['costs'][-1][choice]

    #converting the daily budget into user's currency
    conversionurl = "https://www.budgetyourtrip.com/api/v3/currencies/convert/" + arrivalCurrency + "/" + departureCurrency + "/" + daily_budget
    conversionResponse = requests.request("GET", conversionurl, headers=headers)
    conversion_response_json = json.loads(conversionResponse.text)
    daily_budget_converted = conversion_response_json['data']['newAmount']

    #returns converted daily budget
    return daily_budget_converted
        
    
