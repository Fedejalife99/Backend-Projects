from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.


class Accommodation(models.Model):
    ids = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default=None)
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=30)
    work_zone = models.BooleanField(default=False)
    number_of_rooms = models.IntegerField(default=1)
    number_of_bedrooms = models.IntegerField(default=1)
    space_for_people = models.IntegerField(default=1)
    number_of_stars = models.PositiveBigIntegerField(default=0)
    images = models.ImageField(upload_to="media")
    ocupation = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Reservation(models.Model):
    arrival = models.DateField(default=date.today)
    departure = models.DateField(default=date.today)
    accommodation = models.ForeignKey(
        Accommodation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
