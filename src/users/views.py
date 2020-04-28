from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def sign_in(request):
    return render(request, 'users/sign_in.html', {})
def saved_trips(request):
    return render(request, 'users/saved_trips.html', {})
def view_trip(request):
    return render(request, 'users/view_trip.html', {})