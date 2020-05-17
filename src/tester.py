#!/usr/bin/env python

from django.db.models import Q

import CheepTrips.wsgi
from trips.utils.country_regions import world_regions
from trips.models import Region,Location


while True:
    query = input("Location: ")
    locations = Location.objects.filter(
        Q(airport__icontains=query)|
        Q(country__icontains=query)|
        Q(city__icontains=query)|
        Q(state__icontains=query)).all()
    for location in locations:
        print(location.name())
    print("Count:", len(locations))


# for location in locations:
#     print(location.name())

