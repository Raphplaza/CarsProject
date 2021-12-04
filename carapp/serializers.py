from django.contrib.auth.models import User, Group
from .models import Car, Rate
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    make = serializers.CharField(required=True, allow_blank=False, max_length=50)
    model = serializers.CharField(required=True, allow_blank=False, max_length=50)
    avg_rating = serializers.FloatField(read_only=True, min_value = 0.0, max_value=5.0)
    #rates_number = serializers.IntegerField(read_only=True, min_value=0)

    def create(self, validated_data):
        #Create and return a new `Car` instance, given the validated data.
        return Car.objects.create(**validated_data)

class PopularCarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    make = serializers.CharField(required=True, allow_blank=False, max_length=50)
    model = serializers.CharField(required=True, allow_blank=False, max_length=50)
    rates_number = serializers.IntegerField(read_only=True, min_value=0)




class RateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    car_id = serializers.IntegerField(min_value = 1)
    rating = serializers.FloatField(min_value = 1, max_value=5)

    def create(self, validated_data):
        #Create and return a new `Rate` instance, given the validated data.
        return Rate.objects.create(**validated_data)