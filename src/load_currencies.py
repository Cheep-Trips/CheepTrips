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

currencies = {}
conversions = {'usd':1.0}

def get_conversion(currency):
    if currency in conversions:
        return
    print("Trying: ", currency)
    context = "/currencies/convert/{}/usd"
    if currency.lower() == "usd":
        return
    url = BASE_URL + context.format(currency.lower())
    response = requests.request("GET", url, headers=headers)
    results = response.json()
    if not results['status']:
        return
    if 'data' in results and 'rate' in results['data']:
        rate = results['data']['rate']
        conversions[currency.lower()] = rate


def get_currencies():
    context = "/countries"
    url = BASE_URL + context
    # for region, countries in world_regions.items():
    #     for country in countries:
    #         code = country_codes[country]

    response = requests.request("GET", url, headers=headers)
    results = response.json()
    # print(results)
    for country in results['data']:
        currencies[country['country_code']] = country['currency_code']


get_currencies()

for country,currency in currencies.items():
    get_conversion(currency)

with open('exchange_rates.py', 'w') as f:
    for currency,rate in conversions.items():
        f.write("\t'{}': {},\n".format(currency,rate))
