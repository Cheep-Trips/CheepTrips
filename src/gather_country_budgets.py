#!/usr/bin/env python
import CheepTrips.wsgi
import os
import sys
import json
import requests

from trips.utils.country_codes import country_codes
from trips.utils.curated_regions import world_regions

from trips.models import Location

BASE_URL = "https://www.budgetyourtrip.com/api/v3"

headers = {
        "X-API-KEY": "RIESEWISMERUCSD2020"
    }

countries = {}

def set_budgets(country, budgets):
    if country == "United States":
        country = "United States (US)"
    countries[country] = budgets

def get_country_info(code):
    context = "/costs/country/{}"
    url = BASE_URL + context
    url = url.format(code)
    arrivalResponse = requests.request("GET", url, headers=headers)
    try:
        results = json.loads(arrivalResponse.text)
    except:
        return None
    if not 'data' in results:
        return None
    for category in results['data']:
        if type(category) == dict and 'category_id' in category:
            if category['category_id'] == '0':
                return category
    return None

def get_all_country_info():
    for region, countries in world_regions.items():
        for country in countries:
            code = country_codes[country]
            budgets = get_country_info(code)
            if budgets:
                set_budgets(country, budgets)
                print(country, budgets)
            else:
                print("Missing: ", country)


def get_city_info(city):
    arrivalCity = "London"

    arrivalurl = "https://www.budgetyourtrip.com/api/v3/search/locationdata/" + arrivalCity
    arrivalResponse = requests.request("GET", arrivalurl, headers=headers)
    arrival_response_json = json.loads(arrivalResponse.text)
    print(arrival_response_json)
    sys.exit()

    geonameid = arrival_response_json['data'][0]['geonameid']

    activitiesurl = "https://www.budgetyourtrip.com/api/v3/activities/location/" + geonameid
    activitiesResponse = requests.request("GET", activitiesurl, headers=headers)
    activities_response_json = json.loads(activitiesResponse.text)
    print(activities_response_json)

get_all_country_info()

with open('country_budgets.json', 'w') as f:
    json.dump(countries, f)

