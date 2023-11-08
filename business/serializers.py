from business.models import Business, BusinessComment, BusinessPhoto, Event, EventComment, EventPhoto
from rest_framework import serializers


class BusinessSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Business
        fields = ['id', 'name', 'address', 'city', 'neighbourhood', 'phone', 'logo', 'banner', 'description', 'average_rating']

class BusinessPhotoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = BusinessPhoto
        fields = ['id', 'business', 'photo']


class EventSerializer(serializers.ModelSerializer):
    genre_display = serializers.CharField(source='get_genre_display', read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'business', 'address', 'city', 'neighbourhood', 'title', 'description', 'price', 'datetime', 'artist', 'genre', 'genre_display', 'banner','business_logo']


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventPhoto
        fields = ['id', 'event', 'photo']

class EventCommentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventComment
        fields = ['id', 'event', 'user','user_name','user_logo', 'text','event_name','created_at']


class BusinessCommentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = BusinessComment
        fields = ['id', 'business', 'user', 'user_name','user_logo','text', 'rating','created_at']

