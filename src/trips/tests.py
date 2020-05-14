from django.test import TestCase
from trips.models import *
import datetime
import pytz

# just to test Django TestCase and Travis CI
class TestSumDjango(TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertNotEqual(sum((1, 2, 2)), 6, "This should not be 6.")

# The next several tests are for testing the creation of the modes
class TestRegion(TestCase):

    def test_region_creation(self):
        northAmerica = Region(name="North America")
        asia = Region(name='Asia')

        self.assertEqual(northAmerica.name, 'North America')
        self.assertEqual(asia.name, 'Asia')

class TestLocation(TestCase):

    def setUp(self):
        self.northAmerica = Region(name='North America')
        self.asia = Region(name='Asia')

    def test_location_creation(self):
        losAngeles = Location(exchange_rate=3.8, cost_of_living=75, \
                              region=self.northAmerica)
        tokyo = Location(exchange_rate=1.5, cost_of_living=100, region=self.asia)

        self.assertEqual(losAngeles.exchange_rate, 3.8)
        self.assertEqual(losAngeles.cost_of_living, 75)
        self.assertEqual(losAngeles.region.name, 'North America')
        self.assertEqual(tokyo.exchange_rate, 1.5)
        self.assertEqual(tokyo.cost_of_living, 100)
        self.assertEqual(tokyo.region.name, 'Asia')

class TestActivity(TestCase):
    def setUp(self):
        northAmerica = Region(name='North America')
        asia = Region(name='Asia')

        # must save Location objects to be used in ManyToManyField
        northAmerica.save()
        asia.save()

        self.losAngeles = Location(exchange_rate=3.8, cost_of_living=75, \
                                   region=northAmerica)
        self.tokyo = Location(exchange_rate=1.5, cost_of_living=100, region=asia)
        self.losAngeles.save()
        self.tokyo.save()

    def test_activity_creation(self):
        shopping = Activity(name="Shopping")

        # must save Flight to be able to add Location objects to it
        shopping.save()
        shopping.locations.add(self.losAngeles)
        shopping.locations.add(self.tokyo)

        self.assertEqual(shopping.name, 'Shopping')

        # use <QueryList>[i] to access individual objects of QueryList
        # maybe implement __str__() method  
        self.assertEqual(shopping.locations.all()[0], self.losAngeles)
        self.assertEqual(shopping.locations.all()[1], self.tokyo)
    
class TestFlight(TestCase):

    def setUp(self):
        northAmerica = Region(name='North America')
        asia = Region(name='Asia')
        northAmerica.save()
        asia.save()

        self.losAngeles = Location(exchange_rate=3.8, cost_of_living=75, \
                                   region=northAmerica)
        self.tokyo = Location(exchange_rate=1.5, cost_of_living=100, region=asia)
        self.losAngeles.save()
        self.tokyo.save()

        self.timezone = pytz.timezone("America/Los_Angeles")

    def test_flight_creation(self):

        flight = Flight(departure_location=self.losAngeles, destination=self.tokyo,\
                        flight_carrier="Japan Airlines", \
                        departure_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 8, 0, 0, 0)), \
                        arrival_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 20, 0, 0, 0)), \
                        num_passengers=2, num_bags=4)
        
        self.assertEqual(flight.departure_location, self.losAngeles)
        self.assertEqual(flight.destination, self.tokyo)
        self.assertEqual(flight.flight_carrier, "Japan Airlines")
        self.assertEqual(flight.departure_time, self.timezone.localize( \
                         datetime.datetime(2020, 5, 11, 8, 0, 0, 0)))
        self.assertEqual(flight.arrival_time, self.timezone.localize( \
                         datetime.datetime(2020, 5, 11, 20, 0, 0, 0)))
        self.assertEqual(flight.num_passengers, 2)
        self.assertEqual(flight.num_bags, 4)
        

class TestTrip(TestCase):

    def setUp(self):
        northAmerica = Region(name='North America')
        asia = Region(name='Asia')
        northAmerica.save()
        asia.save()

        self.losAngeles = Location(exchange_rate=3.8, cost_of_living=75, \
                                   region=northAmerica)
        self.tokyo = Location(exchange_rate=1.5, cost_of_living=100, region=asia)
        self.losAngeles.save()
        self.tokyo.save()

        self.timezone = pytz.timezone("America/Los_Angeles")

        self.firstFlight = Flight(departure_location=self.losAngeles, \
                        destination=self.tokyo, flight_carrier="Japan Airlines", \
                        departure_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 8, 0, 0, 0)), \
                        arrival_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 20, 0, 0, 0)), \
                        num_passengers=2, num_bags=4)
        self.secondFlight = Flight(departure_location=self.tokyo, \
                                   destination=self.losAngeles, \
                                   flight_carrier="Japan Airlines", 
                                   departure_time=self.timezone.localize( \
                                   datetime.datetime(2020, 5, 16, 8, 0, 0, 0)), \
                                   arrival_time=self.timezone.localize( \
                                   datetime.datetime(2020, 5, 16, 20, 0, 0, 0)), \
                                   num_passengers=2, num_bags=4)
        self.firstFlight.save()
        self.secondFlight.save()

    def test_trip_creation(self):
        trip = Trip(name="Trip", budget=1000, cost=500)
        trip.save()
        trip.flights.add(self.firstFlight, self.secondFlight)

        self.assertEqual(trip.name, 'Trip')
        self.assertEqual(trip.budget, 1000)
        self.assertEqual(trip.cost, 500)
        self.assertEqual(trip.flights.all()[0], self.firstFlight)
        self.assertEqual(trip.flights.all()[1], self.secondFlight)


    