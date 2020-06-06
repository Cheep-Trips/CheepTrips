#!/usr/bin/env python

from trips.utils.country_regions import world_regions
from trips.utils.country_codes import country_codes

for region, countries in world_regions.items():
    for country in countries:
        if country not in country_codes:
            print("Missing: ", country)


