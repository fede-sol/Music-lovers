from business.models import Business, Event
from rest_framework import serializers


#business serializer
class BusinessSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Business
        fields = ['id', 'name', 'address', 'ciudad', 'barrio', 'phone', 'logo']
class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = ['id', 'business', 'address', 'ciudad', 'barrio', 'title', 'description', 'price', 'datetime', 'artist', 'genre']

