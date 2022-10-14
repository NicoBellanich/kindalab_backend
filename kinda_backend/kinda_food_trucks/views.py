from http.client import HTTPResponse
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from django.core import serializers
from django.forms.models import model_to_dict

import geopy.distance

import pandas as pd

from .models import TruckModel

import json

def index(req):
    return HttpResponse("You're getting default ../food_trucks/ endpoint response")

def get_all_food_trucks_from_database(req):
    all_trucks = list(TruckModel.objects.all().values())
    return JsonResponse(all_trucks, safe=False)

def get_one_food_truck_by_id_from_database(req,food_truck_id):
    try:
        truck_found =model_to_dict(TruckModel.objects.get(pk=food_truck_id))
        return JsonResponse(truck_found, safe=False)
    
    except TruckModel.DoesNotExist:
        raise Http404("No Food Truck matches the given ID.")

def get_sf_api_food_trucks():
    try:
        response= pd.read_json('https://data.sfgov.org/resource/rqzj-sfat.json')
        return response
    except Exception as e:
        raise Exception(type(e))

def get_sf_food_trucks(req):
    return JsonResponse(json.loads(get_sf_api_food_trucks().to_json(orient = 'records')),safe=False)


class HelperCloserFoodTruck():
    def __init__(self,st_name,st_number):
        self._st_name = st_name
        self._st_number = st_number
        self._address = str(st_number)+ " " + st_name + " San Francisco"
        self._address = self._address.replace(" ", "%20")
        self._url = 'https://nominatim.openstreetmap.org/search/' + self._address +'?format=json'

    def calculate_latitude_and_longitude_from_initial_st_name_and_st_number(self):
        try:
            response =  pd.read_json(self._url)
            response = response[response['display_name'].str.lower().str.contains("san francisco")]
            frist_one_approach = 0
            lat = response.iloc[frist_one_approach]["lat"]
            lon = response.iloc[frist_one_approach]["lon"]
            self._lat = lat
            self._lon = lon
        
        except Exception as e:
            raise Exception(type(e))

    def calculate_closer_food_truck_from_initial_lat_and_lon(self):
        
        trucks = get_sf_api_food_trucks()
        shorter_distance = 10000000000000
        shorter_index = 0
        coords_1 = (self._lat,self._lon)
        for index in trucks.index:
            coords_2 = (trucks["latitude"][index],trucks["longitude"][index])
            distance = geopy.distance.geodesic(coords_1, coords_2).km
            if distance < shorter_distance:
                shorter_distance = distance
                shorter_index = index
        shorter_distance = round(shorter_distance,2)
        
        self.closer_food_truck_result = {
            "closerKMDistance" : shorter_distance,
            "initialLatitude" : self._lat,
            "initialLongitude" : self._lon,
            "finalLatitude" : trucks["latitude"][shorter_index],
            "finalLongitude" : trucks["longitude"][shorter_index]
        }

def calculate_closer_food_truck(req,st_number,st_name):

    helperCloserFoodTruck = HelperCloserFoodTruck(st_number=st_number,st_name=st_name)

    helperCloserFoodTruck.calculate_latitude_and_longitude_from_initial_st_name_and_st_number()

    helperCloserFoodTruck.calculate_closer_food_truck_from_initial_lat_and_lon()

    return JsonResponse(helperCloserFoodTruck.closer_food_truck_result,safe=False)
