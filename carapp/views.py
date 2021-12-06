import re
from django.shortcuts import render

from rest_framework import serializers, viewsets
from rest_framework import permissions
from carapp.serializers import CarSerializer, RateSerializer, PopularCarSerializer
from carapp.models import Car, Rate

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from carapp.validators import car_make_exists, car_model_exists

@api_view(['GET','POST'])
def car_list(request, format=None):
    """
    List all code cars, or create a new car.
    """
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            if car_make_exists(request) and car_model_exists(request):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST','DELETE'])
def car_detail(request, pk,format=None):
    """
    GET, POST or DELETE a car.
    """
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        car.delete()
        return Response(status=204)

    elif request.method == 'POST':
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            if car_make_exists(request) and car_model_exists(request):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def rate_list(request, pk,format=None):
    """
    View all reviews of single car
    """
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        rate = car.rate_set.all()
        serializer = RateSerializer(rate, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def rate(request, format=None):

    if request.method == 'POST':
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def car_list_popular(request, format=None):
    """
    List of top cars, based on number of ratings (not average!)
    """
    if request.method == 'GET':

        cars = Car.objects.all()

        #sort by func 'rates_number' 
        sorted_cars = sorted(cars, key= lambda car: -(car.rates_number()))

        #top 5 of sorted
        sorted_cars = sorted_cars[:5]

        serializer = PopularCarSerializer(sorted_cars, many=True)
        return Response(serializer.data)