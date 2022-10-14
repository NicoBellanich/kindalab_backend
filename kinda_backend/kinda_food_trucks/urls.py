from django.urls import path

from . import views


# This URLS will came from Project URLS path and index all paths I writte here

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.get_all_food_trucks_from_database, name="all_db"),
    path("<int:food_truck_id>/",
         views.get_one_food_truck_by_id_from_database, name="by_id"),
    path("sf_food_trucks", views.get_sf_food_trucks, name="sf_trucks"),
    path("<int:st_number>/<str:st_name>",
         views.calculate_closer_food_truck, name="closer"),
]
