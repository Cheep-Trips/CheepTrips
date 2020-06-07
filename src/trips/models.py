from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=200)
    

class Location(models.Model):
    airport = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, blank=True, null=True)
    exchange_rate = models.IntegerField(default=1)
    cost_of_living = models.IntegerField(default=0)
    region =  models.ForeignKey(Region, on_delete=models.CASCADE)
    budget = models.IntegerField(default=20)
    midrange = models.IntegerField(default=50)
    luxury = models.IntegerField(default=100)

    def __str__(self):
        return self.name()

    def name(self):
        if self.state:
            return "{}, {} {} ({})".format(self.city, self.state, self.country, self.airport)
        return "{}, {} ({})".format(self.city, self.country, self.airport)



class Activity(models.Model):
    name = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location)

class User(AbstractUser):
    pass    

class Trip(models.Model):
    name = models.CharField(max_length=200, blank=True)
    budget = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    num_passengers = models.IntegerField(default=1)
    num_bags = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='trips')


class Flight(models.Model):
    departure_location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='departures')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='arrivals')
    flight_carrier = models.CharField(max_length=200)
    departure_time = models.DateTimeField('Departure date')
    arrival_time = models.DateTimeField('Arrival date')
    price = models.IntegerField(default=0)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,related_name='flights')

