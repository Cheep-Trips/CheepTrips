import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy

# from amadeus import Client, ResponseError

from .forms import WelcomeForm


class WelcomeView(FormView):
    form_class=WelcomeForm
    success_url=reverse_lazy('trips:view_flight')
    template_name='trips/welcome_form.html'

    def form_valid(self, form):
        departure = form.cleaned_data['departure']
        destination = form.cleaned_data['destination']
        self.success_url = "{}?departure={}&destination={}".format(self.success_url, departure, destination)
        return super().form_valid(form)


# Create your views here.
def welcome(request):

    # amadeus = Client(
    #     client_id=os.getenv("AMADEUS_KEY"),
    #     client_secret=os.getenv("AMADEUS_SECRET"),
    # )
    # try:
    #     response = amadeus.shopping.flight_offers_search.get(
    #         originLocationCode='SYD',
    #         destinationLocationCode='BKK',
    #         departureDate='2020-07-01',
    #         adults=1)
    #     return HttpResponse(response.data)
    # except ResponseError as error:
    #     print(error)
    # return HttpResponse("<html>ERROR</html>")

    return render(request, 'trips/welcome.html', {})


def destination(request):
    return render(request, 'trips/destination.html', {})
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
def forgot_password(request):
    return render(request, 'trips/forgot_password.html', {})
def view_flight(request):
    return render(request, 'trips/view_flight.html', {})