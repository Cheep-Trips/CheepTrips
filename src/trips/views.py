import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy

from django_registration.backends.one_step.views import RegistrationView as BaseRegistrationView
from .forms import NewAccountForm


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

        #skyscanner to cache call here 
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

        #skyscanner call to live here
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


class RegistrationView(BaseRegistrationView):
    form_class=NewAccountForm
    success_url=reverse_lazy('trips:welcome')

    def get_form(self, form_class=None):
     data = super().get_form(form_class)
     for field in data.fields:
        print(dir(field))
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


def getSkyscannerCached(request):

    departure = departure
    departure_date = departure_date
    inbound_date = return_date
 
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/US/USD/en-US/" + departure + "-sky/" + arrival + "/" + departure_date
 
    querystring = {"inboundpartialdate":inbound_date}
 
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': SKYSCANNER_API_KEY
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)

    response_json = json.loads(response.text)
 
    places = response_json['Places']
    places_dict = {}

    for place in places:
        places_dict[place['PlaceId']] = place['SkyscannerCode']
    
    for quote in response_json['Quotes']:
        print('Flight to ' + places_dict[quote['OutboundLeg']['DestinationId']] + ' Costs ' + str(quote['MinPrice']))

def getSkyscannerLive(request, this):
    response = unirest.post("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",
    headers={
        "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        "X-RapidAPI-Key": SKYSCANNER_API_KEY
        "Content-Type": "application/x-www-form-urlencoded"
     },
    params={
        "inboundDate": this.departure_date,
        "cabinClass": "economy",
        "children": "0",
        "infants": "0",
        "country": this.country,
        "currency": "USD",
        "locale": "en-US",
        "originPlace": form.originPlace +"-sky"
        "destinationPlace": form.destinationPlace +"-sky"
        "outboundDate": form.return_date
        "adults": form.travelers
    })

    response = unirest.get("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/{sessionkey}?pageIndex=0&pageSize=10",
  headers={
    "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "SIGN-UP-FOR-KEY"
  }
)

def getEchangeRate(request):
    url = 'https://open.exchangerate-api.com/v6/latest/USD'

    # Here is all the exchange rates to all countries from USD
    response = requests.get(url)
    data = response.json()

    return data

def getBudget(request, city):
    #todo (most likely over the weekend)

    url = https://www.budgetyourtrip.com/api/v3/search/locationdata/ + city
    response = requests.post( url, headers=headers, auth=("apikey", BUDGET_YOUR_TRIP_API_KEY))