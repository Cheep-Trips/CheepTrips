from django.db import models

# Create your models here.

class Region(models.Model):
    region = models.CharField(max_length=200)
    

class Location(models.Model):
    exchange_rate = models.IntegerField(default=1)
    cost_of_living = models.IntegerField(default=0)
    regions =  models.ForeignKey(Region, on_delete=models.CASCADE)

class Activities(models.Model):
    activity = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location)

class Flights(models.Model):
    start_airport = models.CharField(max_length=200)
    dest_airport = models.OneToOneField(
        Location,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    flight_carrier = models.CharField(max_length=200)
    departure_time = models.DateTimeField('Departure date')
    arrival_time = models.DateTimeField('Arrival date')
    num_passengers = models.IntegerField(default=1)
    num_bags = models.IntegerField(default=1)

class Trips(models.Model):
    budget = models.IntegerField(default=0)
    total_cost = models.IntegerField(default=0)
    flight_list = models.ManyToManyField(Flights)    

    



class User(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    