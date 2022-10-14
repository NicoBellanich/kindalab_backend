import pytest

from kinda_food_trucks.views import HelperCloserFoodTruck


class AddressInfo():
    def __init__(self, st_name, st_number, real_latitude=0, real_longitude=0, closer_food_truck_km_distance=0):
        self.st_name = st_name
        self.st_number = st_number
        self.real_latitude = real_latitude
        self.real_longitude = real_longitude
        self.closer_food_truck_km_distance = closer_food_truck_km_distance


def test_calculate_latitude_and_longitude_from_initial_st_name_and_st_number():
    # GIVEN some real address directions taken from real API results
    address_directions = [AddressInfo(st_name="BATTERY", st_number=111, real_latitude=37.79236678688307, real_longitude=-122.40014830676716), AddressInfo(
        st_name="GROVE", st_number=1265, real_latitude=37.775774368410254, real_longitude=-122.43733160784082), AddressInfo(st_name="MARKET", st_number=532, real_latitude=37.79054831818324, real_longitude=-122.40033367367877)]

    # WHEN iterate over each address direction
    for address_info in address_directions:
        helper = HelperCloserFoodTruck(
            address_info.st_name, address_info.st_number)
        # AND calculate latitude and longitude from initial st name and number for each address
        helper.calculate_latitude_and_longitude_from_initial_st_name_and_st_number()

        # THEN latitude and longitude should be closer from real one given by the api
        assert abs(helper._initial_latitude -
                   address_info.real_latitude) <= 0.1
        assert abs(helper._initial_longitude -
                   address_info.real_longitude) <= 0.1


def test_calculate_closer_food_truck_from_initial_lat_and_lon():
    # GIVEN some addressess with theirs st name, st number and known food truck closer distance
    address_directions = [AddressInfo(st_name="BATTERY", st_number=100, closer_food_truck_km_distance=0.04), AddressInfo(
        st_name="GROVE", st_number=1250, closer_food_truck_km_distance=0.05), AddressInfo(st_name="MARKET", st_number=500, closer_food_truck_km_distance=0.1)]

    # WHEN iterate over each address direction
    for address_info in address_directions:

        helper = HelperCloserFoodTruck(
            address_info.st_name, address_info.st_number)
        helper.calculate_latitude_and_longitude_from_initial_st_name_and_st_number()

        # AND calculate closer food truck for each address
        helper.calculate_closer_food_truck_from_initial_lat_and_lon()

        # THEN closer distance calculated should be closer to known closer distance
        assert abs(helper.closer_food_truck_result["closerKMDistance"] - address_info.closer_food_truck_km_distance) <= 0.1
