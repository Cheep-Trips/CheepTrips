from django.db import models

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

    def name(self):
        if self.state:
            return "{}, {} {} ({})".format(self.city, self.state, self.country, self.airport)
        return "{}, {} ({})".format(self.city, self.country, self.airport)



class Activity(models.Model):
    name = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location)


class Flight(models.Model):
    departure_location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='departures')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='arrivals')
    flight_carrier = models.CharField(max_length=200)
    departure_time = models.DateTimeField('Departure date')
    arrival_time = models.DateTimeField('Arrival date')


class Trip(models.Model):
    name = models.CharField(max_length=200)
    budget = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    flights = models.ManyToManyField(Flight)    
    num_passengers = models.IntegerField(default=1)
    num_bags = models.IntegerField(default=1)
    
# class User(models.Model):
#     email = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
    