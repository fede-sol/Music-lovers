from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from business.models import Business

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = get_user_model()
        fields = ['id', 'email', 'username', 'password','user_type','logo']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:

        res = super().validate(attrs)

        return {'access':res['access']}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username
        if user.user_type == 1:
            try:
                business = Business.objects.get(user=user)

                token['business_id'] = business.id
                if business.logo.url:
                    token['logo'] = business.logo.url

            except Business.DoesNotExist:
                token['business_id'] = None
        else:
            if user.logo.url:
                token['logo'] = user.logo.url
        token['user_type'] = user.user_type

        return token