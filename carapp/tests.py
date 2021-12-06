# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from carapp.models import Car, Rate
import random
import statistics

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CarSerializer, RateSerializer

from rest_framework.test import APIRequestFactory

# initialize the APIClient app
client = Client()

#Endpoints Test

class GetEndpointsTests(TestCase):

    def setUp(self):
        Car.objects.create(
            make='audi', model="a4")
        Car.objects.create(
            make='audi', model="a6")
        Car.objects.create(
            make='audi', model="a8")

        rating1=random.randint(1,5)
        rating2=random.randint(1,5)
        rating3=random.randint(1,5)

        Rate.objects.create(
            car_id=1, rating = rating1)
        Rate.objects.create(
            car_id=1, rating = rating2)
        Rate.objects.create(
            car_id=1, rating = rating3)        

    def test_get_all_cars(self):
        # get API response
        response = client.get('/cars/')
        # get data from db
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_all_rates(self):
        # get API response
        response = client.get('/rates/1/')
        # get data from db
        rates = Rate.objects.filter(car_id=1)
        serializer = RateSerializer(rates, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_avg_rating(self):
        # get API response
        response = client.get('/cars/1/')
        # get data from db
        rates = Rate.objects.all()
        ratings = []
        for rate in rates:
            ratings.append(rate.rating)
        average_rating = statistics.mean(ratings)
        self.assertEqual(response.data["avg_rating"], average_rating)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_num_of_rating(self):
        # get API response
        response = client.get('/rates/1/')
        # get data from db
        rates = Rate.objects.filter(car_id=1)
        serializer = RateSerializer(rates, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PopularViewTests(TestCase):

    def setUp(self):
        Car.objects.create(
            make='audi', model="a4")
        Car.objects.create(
            make='audi', model="a6")
        Car.objects.create(
            make='audi', model="a8")

        rating1=random.randint(1,5)
        rating2=random.randint(1,5)
        rating3=random.randint(1,5)

        for i in range(1,80):
            Rate.objects.create(
                car_id=1, rating = rating1)

        #most ratings for the car with id=2 (audi a6)
        for i in range(1,100): 
            Rate.objects.create(
                car_id=2, rating = rating2)

        for i in range(1,60): 
            Rate.objects.create(
                car_id=3, rating = rating3)   

    def test_popular_cars(self):
        # get API response
        response = client.get('/popular')

        self.assertEqual(response.data[0]['model'], "a6")
        self.assertEqual(response.data[1]['model'], "a4")
        self.assertEqual(response.data[2]['model'], "a8")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostEndpointsTests(TestCase):
    def test_post_car(self):
        request = client.post('/cars/', {"make": "audi","model":"A6"}, format='json')
        request = client.post('/cars/', {"make": "audi","model":"A4"}, format='json')
        request = client.post('/cars/', {"make": "audi","model":"A8"}, format='json')

        #creating a non-existing car
        request = client.post('/cars/', {"make": "auuuudi","model":"A8"}, format='json')

        # get data from db
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(serializer.data[0]["make"],"audi")
        self.assertEqual(serializer.data[1]["model"],"A4")
        self.assertEqual(len(serializer.data),3)


    
#Basic Backend test

class RateModelTests(TestCase):
    def test_number_of_rates(self):
        
        Car.objects.create(make='volkswagen',model='polo')
        for i in range(1,21):
            Rate.objects.create(car_id=1,rating=4)

        self.assertEqual(len(Car.objects.get(id=1).rate_set.all()),20)

