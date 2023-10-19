from ml_auth.models import MusicLoversUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer


class BusinessSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_user_model().objects.get(email=request.data['email'])
            user.set_password(request.data['password'])
            user.user_type = 1  # Set user type as business
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)})

        return Response(serializer.errors, status=status.HTTP_200_OK)


class BusinessLoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(email=request.data['email'])
            if user.user_type == 1:  # Allow business users to log in
                response = super().post(request, *args, **kwargs)
            else:
                response = Response(
                    {'detail': 'Access denied for this user type.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except MusicLoversUser.DoesNotExist:
            response = Response(
                {'detail': 'No user with this email exists.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return response




