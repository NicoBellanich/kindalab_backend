from http.client import HTTPResponse
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from django.core import serializers
from django.forms.models import model_to_dict

import geopy.distance

import pandas as pd

from .models import TruckModel

import json

def index(req):
    """
    Default response from /food_trucks/ path
    
    Arguments:
        None
    Returns:
        String
    """
    return HttpResponse("You're getting default ../food_trucks/ endpoint response")

def get_all_food_trucks_from_database(req):
    """
    Get all database Truck objects from Database Models
    
    Arguments:
        None
    Returns:
        JsonResponse
    """
    all_trucks = list(TruckModel.objects.all().values())
    return JsonResponse(all_trucks, safe=False)

def get_one_food_truck_by_id_from_database(req,food_truck_id):
    """
    Get one database Truck object from Database Models by given ID
    
    Arguments:
        None
    Returns:
        JsonResponse | Http404
    """
    try:
        truck_found =model_to_dict(TruckModel.objects.get(pk=food_truck_id))
        return JsonResponse(truck_found, safe=False)
    
    except TruckModel.DoesNotExist:
        raise Http404("No Food Truck matches the given ID.")

def get_sf_api_food_trucks():
    """
    Helper Function to get external San Francisco API food trucks

    Arguments:
    None
    Returns:
    pd.DataFrame | Exception
    """
    try:
        response= pd.read_json('https://data.sfgov.org/resource/rqzj-sfat.json')
        return response
    except Exception as e:
        raise Exception(type(e))

def get_sf_food_trucks(req):
    """
    Get San Francisco Food Trucks JSON
    
    Arguments:
        None
    Returns:
        JsonResponse 
    """
    return JsonResponse(json.loads(get_sf_api_food_trucks().to_json(orient = 'records')),safe=False)


class HelperCloserFoodTruck():
    """
    Helper class for the steps of calculate_closer_food_truck() functionality
    """
    def __init__(self,st_name,st_number):
        self._st_name = st_name
        self._st_number = st_number
        self._address = str(st_number)+ " " + st_name + " San Francisco"
        self._address = self._address.replace(" ", "%20")
        self._api_to_get_lat_and_lon_by_given_address = 'https://nominatim.openstreetmap.org/search/' + self._address +'?format=json'

    def calculate_latitude_and_longitude_from_initial_st_name_and_st_number(self):
        """
        Calculate and set the latitude and longitude of some point by sending the street name and street number
        
        Arguments:
            None
        Returns:
            None
        """
        try:
            response =  pd.read_json(self._api_to_get_lat_and_lon_by_given_address)
            response = response[response['display_name'].str.lower().str.contains("san francisco")]
            frist_one_approach = 0
            lat = response.iloc[frist_one_approach]["lat"]
            lon = response.iloc[frist_one_approach]["lon"]
            self._initial_latitude = lat
            self._initial_longitude = lon
        
        except Exception as e:
            raise Exception(type(e))

    def calculate_closer_food_truck_from_initial_lat_and_lon(self):
        """
        Calculate and set the closer food truck from some initial latitude and longitude initial coordinate
        
        Arguments:
            None
        Returns:
            None
        """
        trucks = get_sf_api_food_trucks()
        shorter_distance = 10000000000000
        shorter_index = 0
        coords_1 = (self._initial_latitude,self._initial_longitude)
        for index in trucks.index:
            coords_2 = (trucks["latitude"][index],trucks["longitude"][index])
            distance = geopy.distance.geodesic(coords_1, coords_2).km
            if distance < shorter_distance:
                shorter_distance = distance
                shorter_index = index
        shorter_distance = round(shorter_distance,2)
        
        self.closer_food_truck_result = {
            "closerKMDistance" : shorter_distance,
            "initialLatitude" : self._initial_latitude,
            "initialLongitude" : self._initial_longitude,
            "finalLatitude" : trucks["latitude"][shorter_index],
            "finalLongitude" : trucks["longitude"][shorter_index]
        }

def calculate_closer_food_truck(req,st_number,st_name):
    """
    Calculate and returns closer food truck in San Francisco (California,USA) by a given street number and street name
    
    Arguments:
        st_number: int
        st_name: String
    Returns:
        JsonResponse
    """
    helperCloserFoodTruck = HelperCloserFoodTruck(st_number=st_number,st_name=st_name)

    helperCloserFoodTruck.calculate_latitude_and_longitude_from_initial_st_name_and_st_number()

    helperCloserFoodTruck.calculate_closer_food_truck_from_initial_lat_and_lon()

    return JsonResponse(helperCloserFoodTruck.closer_food_truck_result,safe=False)
