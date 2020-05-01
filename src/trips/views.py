from django.shortcuts import render
from django.http import HttpResponse
from amadeus import Client, ResponseError
import os
# Create your views here.
def start(request):

    amadeus = Client(
        client_id=os.getenv("AMADEUS_KEY"),
        client_secret=os.getenv("AMADEUS_SECRET"),
    )
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode='SYD',
            destinationLocationCode='BKK',
            departureDate='2020-07-01',
            adults=1)
        return HttpResponse(response.data)
    except ResponseError as error:
        print(error)
    return HttpResponse("<html>ERROR</html>")

    #return render(request, 'trips/start.html', {})
def dest(request):
    return render(request, 'trips/dest.html', {})
def sign_in(request):
    return render(request, 'trips/sign_in.html', {})
def saved_trips(request):
    return render(request, 'trips/saved_trips.html', {})
def view_trip(request):
    return render(request, 'trips/view_trip.html', {})