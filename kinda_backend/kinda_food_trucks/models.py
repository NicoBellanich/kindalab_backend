from email.policy import default
from pyexpat import model
from time import timezone
from django.db import models

class TruckModel(models.Model):
    # Need to specify attributes and default values
    applicant = models.TextField(default=" ")
    facilitytype = models.TextField(default=" ")
    locationdescription = models.TextField(default=" ")
    address = models.TextField(default=" ")
    status = models.TextField(default=" ")
    latitude = models.FloatField(default=0.0,max_length=200)
    longitude = models.FloatField(default=0.0,max_length=200)
    expirationdate = models.DateField("expiration date")

    # This just replace the returning of < Truck obj > by <QuerySet [<Truck: prueba>]>
    def __str__(self):
        return self.address

    def status_is_approbed(self):
        return self.status == 'APPROVED'

    def is_expired(self):
        return self.expirationdate < timezone.now()

class TestModel(models.Model):
    name = models.TextField(default=" ")

    def __str__(self):
        return self.name

