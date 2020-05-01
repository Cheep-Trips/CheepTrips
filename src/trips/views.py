from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def start(request):
    return render(request, 'trips/start.html', {})
def dest(request):
    return render(request, 'trips/dest.html', {})
def sign_in(request):
    return render(request, 'trips/sign_in.html', {})
def saved_trips(request):
    return render(request, 'trips/saved_trips.html', {})
def view_trip(request):
    return render(request, 'trips/view_trip.html', {})