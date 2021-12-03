from django.db import models
from datetime import timedelta
from django.db.models.fields import FloatField
from django.utils import timezone
from time import time
from django.db.models import Avg

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Car(models.Model):
    make = models.CharField('make', max_length=50)
    model = models.CharField('car model',max_length=50)
    avg_rating = FloatField('average rating', default=0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return self.make + ' ' + self.model 

    def avg_rating(self):
        return self.rate_set.all().aggregate(Avg('rating'))['rating__avg']


class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField('rating', validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __int__(self):
        return self.rating