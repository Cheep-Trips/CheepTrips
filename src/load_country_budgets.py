#!/usr/bin/env python
import CheepTrips.wsgi
import os
import sys
import json

from trips.utils.exchange_rates import exchange_rates
from trips.utils.curated_regions import world_regions

from trips.models import Location

BASE_URL = "https://www.budgetyourtrip.com/api/v3"

headers = {
        "X-API-KEY": "RIESEWISMERUCSD2020"
    }

def set_budgets(country, budgets):
    print("Trying: ", country, end='')
    code = budgets['country_code'].lower()
    if not code in exchange_rates:
        print(", rate not found for country code {}.".format(code))
        return
    rate = float(exchange_rates[code])
    if not rate:
        return
    value_budget = float(budgets['value_budget'])/rate
    value_midrange = float(budgets['value_midrange'])/rate
    value_luxury = float(budgets['value_luxury'])/rate
    try:
        budget = int(value_budget)
        midrange = int(value_midrange)
        luxury = int(value_luxury)
    except:
        return
    locations = Location.objects.filter(country__startswith=country).all()
    print(", Finished with {} locations.".format(len(locations)))
    for location in locations:
        location.budget = budget
        location.midrange = midrange
        location.luxury = luxury
        location.save()

def load_countries():
    with open('country_budgets.json') as f:
        data = json.load(f)
        for country,budgets in data.items():
            set_budgets(country, budgets)

load_countries()