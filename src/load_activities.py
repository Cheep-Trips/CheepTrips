#!/usr/bin/env python

# Whistler, British Columbia YVR Vancouver
# Courchevel, France LYS Lyon or GVA Geneva
# Valais, Switzerland 
# Vail, Colorado,USA EGE or DEN
# Aspen, Colorado, USA   ASE or DEN
# Tarentaise Valley, France GVA Geneva
# Cortina d’Ampezzo,Italy VCE Venice
# Mammoth Lakes - San Jose SJC
# SEA Seattle

import CheepTrips.wsgi

from trips.models import Location, Activity

name = "Skiing/Snowboarding"
airports = [
    'GVA', 
    'YVR',
    'DEN',
    'VCE',
    'SEA'
]

activity = Activity(name=name)
activity.save()

for airport in airports:
    location = Location.objects.get(airport=airport)
    activity.locations.add(location)

