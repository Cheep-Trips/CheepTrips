#!/usr/bin/env python

import CheepTrips.wsgi
from trips.utils.country_regions import world_regions
from trips.models import Region,Location
from trips.utils.us_airports import us_airports
from trips.utils.canadian_airports import canadian_airports
from trips.utils.intl_airports import intl_airports

# load regions
regions = {}
for k,v in world_regions.items():
    region, created = Region.objects.get_or_create(name=k)
    regions[k] = region
for k,v in regions.items():
    print(k,v)

# load US
for airport in us_airports:
    region = regions["North America"]
    city = airport[0]
    airport_str = airport[2]
    state = airport[1]
    country = "United States (US)"
    location, created = Location.objects.get_or_create(
        airport=airport_str,
        country=country,
        city=city,
        state=state,
        region=region
    )   
# load Canada
for airport in canadian_airports:
    region = regions["North America"]
    city = airport[0]
    airport_str = airport[2]
    state = airport[1]
    country = "Canada"
    location, created = Location.objects.get_or_create(
        airport=airport_str,
        country=country,
        city=city,
        state=state,
        region=region
    )   
# load intl
for airport in intl_airports:
    region = regions[airport[0]]
    city = airport[2]
    airport_str = airport[3]
    country = airport[1]
    location, created = Location.objects.get_or_create(
        airport=airport_str,
        country=country,
        city=city,
        region=region
    )   
