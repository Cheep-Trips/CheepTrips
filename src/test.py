#!/usr/bin/env python
import CheepTrips.wsgi
import os
import sys

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, RedirectView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin





import requests, json
from collections import OrderedDict

import datetime

headers = {
        "X-API-KEY": "RIESEWISMERUCSD2020"
    }

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
