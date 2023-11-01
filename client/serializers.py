from client.models import UserPreferences
from rest_framework import serializers



class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['id', 'user', 'genre']