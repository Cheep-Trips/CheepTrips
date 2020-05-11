from django.db import models

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=200)
    

class Location(models.Model):
    exchange_rate = models.IntegerField(default=1)
    cost_of_living = models.IntegerField(default=0)
    region =  models.ForeignKey(Region, on_delete=models.CASCADE)

class Activity(models.Model):
    name = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location)

class Flight(models.Model):
    departure_location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='departures')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='arrivals')
    flight_carrier = models.CharField(max_length=200)
    departure_time = models.DateTimeField('Departure date')
    arrival_time = models.DateTimeField('Arrival date')
    num_passengers = models.IntegerField(default=1)
    num_bags = models.IntegerField(default=1)

class Trip(models.Model):
    name = models.CharField(max_length=200)
    budget = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    flights = models.ManyToManyField(Flight)    

    
# class User(models.Model):
#     email = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
    