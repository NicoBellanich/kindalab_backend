# Generated by Django 4.1.1 on 2022-10-07 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kinda_food_trucks', '0003_test_name_truck_address_truck_applicant_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Test',
            new_name='TestModel',
        ),
        migrations.RenameModel(
            old_name='Truck',
            new_name='TruckModel',
        ),
    ]