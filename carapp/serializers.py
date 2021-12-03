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


"""
class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['make', 'model']
"""

class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    make = serializers.CharField(required=True, allow_blank=False, max_length=50)
    model = serializers.CharField(required=True, allow_blank=False, max_length=50)

    def create(self, validated_data):
        
        #Create and return a new `Car` instance, given the validated data.
       
        return Car.objects.create(**validated_data)
