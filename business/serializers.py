from business.models import Business, BusinessPhoto, Event, EventPhoto
from rest_framework import serializers


class BusinessSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Business
        fields = ['id', 'name', 'address', 'ciudad', 'barrio', 'phone', 'logo']

class BusinessPhotoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = BusinessPhoto
        fields = ['id', 'business', 'photo']


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = ['id', 'business', 'address', 'ciudad', 'barrio', 'title', 'description', 'price', 'datetime', 'artist', 'genre','banner']

class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventPhoto
        fields = ['id', 'event', 'photo']

