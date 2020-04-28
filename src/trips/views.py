from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def start(request):
    return render(request, 'trips/start.html', {})
def dest(request):
    return render(request, 'trips/dest.html', {})
