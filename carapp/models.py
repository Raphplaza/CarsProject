from django.db import models
from datetime import timedelta
from django.utils import timezone
from time import time

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Car(models.Model):
    make = models.CharField('make', max_length=50)
    model = models.CharField('car model',max_length=50)



class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.FloatField('rating', validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])