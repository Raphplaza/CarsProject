from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from carapp.serializers import UserSerializer, GroupSerializer, CarSerializer
from carapp.models import Car, Rate

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST','DELETE'])
def car_detail(request, pk,format=None):
    """
    GET, or DELETE a car.
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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





"""
#old views
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    
    #API endpoint that allows groups to be viewed or edited.
   
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarViewSet(viewsets.ModelViewSet):
   
    #API endpoint that allows cars to be viewed or edited.
    
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
"""
