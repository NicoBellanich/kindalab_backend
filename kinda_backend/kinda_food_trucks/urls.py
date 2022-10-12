from django.urls import path

from . import views


#This URLS will came from Project URLS path and index all paths I writte here

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all_trucks, name="all"),
    path("other_api", views.other_api_trucks, name="other"),
    path("<int:truck_id>/", views.one_truck, name="by_id"),
    path("<int:st_number>/<str:st_name>", views.calculate_closer_food_truck, name="closer"),
]