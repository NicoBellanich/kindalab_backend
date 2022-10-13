from http.client import HTTPResponse
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from django.core import serializers
from django.forms.models import model_to_dict

import geopy.distance

import pandas as pd

from .models import TruckModel

def index(req):
    return HttpResponse("You're on the main page")

def all_trucks(req):
    #selected_truck = TruckModel.objects.filter()
   
    all_trucks = list(TruckModel.objects.all().values())
    return JsonResponse(all_trucks, safe=False) # With safe=False it's no needed to do JsonResponse({"data": list(all_trucks)})


def one_truck(req,truck_id):
    try:
        truck_found =model_to_dict(TruckModel.objects.get(pk=truck_id))
        return JsonResponse(truck_found, safe=False)
    
    except TruckModel.DoesNotExist:
        raise Http404("No TruckModel matches the given query.")

def get_other_api_trucks():
    try:
        response= pd.read_json('https://data.sfgov.org/resource/rqzj-sfat.json')
        return response
    except Exception as e:
        raise Exception(type(e))

def other_api_trucks(req):
    return get_other_api_trucks()

def get_latitude_float(latitude):
    try:
        latitude = float(latitude)
    except ValueError:
        return HttpResponseNotFound(
            "'Latitude' must be convertible to an integer.")
    return latitude

def get_longitude_float(longitude):
    try:
        longitude = float(longitude)
    except ValueError:
        return HttpResponseNotFound(
            "'Longitude' must be convertible to an integer.")
    return longitude

def check_latitude_and_longitude(latitude,longitude):
    print(latitude)
    if latitude < -90 or latitude > 90:
        raise HttpResponseNotFound(
            "'Latitude' must be betweeen -90 and 90 boundaries.")
    print(longitude)
    if longitude < -180 or longitude > 180:
        raise HttpResponseNotFound(
            "'Longitude' must be betweeen -90 and 90 boundaries.")

def calculate_closer_food_truck(req,st_number,st_name):

    # latitude = get_latitude_float(latitude=latitude)
    # longitude = get_longitude_float(longitude=longitude)
    
    # print("LAT",latitude)
    # print("LONG",longitude)
    
    #TODO
    #check_latitude_and_longitude(latitude=latitude,longitude=longitude)

    address = str(st_number)+ " " + st_name + " San Francisco"
    address = address.replace(" ", "%20")
    url = 'https://nominatim.openstreetmap.org/search/' + address +'?format=json'

    try:
        response =  pd.read_json(url)
        response = response[response['display_name'].str.lower().str.contains("san francisco")]
        frist_one_approach = 0
        lat = response.iloc[frist_one_approach]["lat"]
        lon = response.iloc[frist_one_approach]["lon"]

    except Exception as e:
        raise Exception(type(e))

    # TO KNOW LAT AND LONG OF FOOD TRUCK FROM ST NUMBER AND ST NAME
    #return HttpResponse(f"the lat {lat} and the lon {lon}")


    trucks = get_other_api_trucks()
    shorter_distance = 10000000000000
    shorter_index = 0
    coords_1 = (lat,lon)
    for index in trucks.index:
        coords_2 = (trucks["latitude"][index],trucks["longitude"][index])
        distance = geopy.distance.geodesic(coords_1, coords_2).km
        if distance < shorter_distance:
            shorter_distance = distance
            shorter_index = index
    shorter_distance = round(shorter_distance,2)
    return HttpResponse(f"OKK, the shorter distance is {shorter_distance} km and the index is {shorter_index}")