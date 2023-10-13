from business.models import Event
from rest_framework import serializers



class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = ['id', 'business', 'address', 'ciudad', 'barrio', 'title', 'description', 'price', 'datetime', 'artist', 'genre']

