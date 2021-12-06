from urllib import request
from bs4 import BeautifulSoup
import json
from rest_framework import serializers

def car_make_exists(serializer):
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    site_json=json.loads(soup.text)

    make_list = []
    for result in site_json['Results']:
        make_list.append(result['Make_Name'].lower())

    if serializer.data["make"].lower() in make_list:
        return True
    else:
        return False

def car_model_exists(serializer):
    car_make = serializer.data["make"].lower()
    url = 'https://vpic.nhtsa.dot.gov/api///vehicles/GetModelsForMake/' + car_make + '?format=json'
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    site_json=json.loads(soup.text)

    model_list = []
    for result in site_json['Results']:
        model_list.append(result['Model_Name'].lower())

    if serializer.data["model"].lower() in model_list:
        return True
    else:
        return False
