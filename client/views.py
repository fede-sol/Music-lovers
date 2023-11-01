from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from business.models import Business
from business.serializers import BusinessSerializer
from client.models import UserPreferences
from client.serializers import UserPreferenceSerializer
from ml_auth.models import MusicLoversUser
from ml_auth.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework import status



class ModifyClientProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        if user.user_type == 2:

            request.data._mutable = True
            data = request.data

            dict = {'logo':data['logo']}

            if 'logo' in data:
                serializer = UserSerializer(instance=user, data=dict, partial=True)
                del data['logo']

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            try:
                preferences = UserPreferences.objects.get(user=user)
            except UserPreferences.DoesNotExist:
                return Response({'error': 'El usuario no posee preferencias asignadas'}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserPreferenceSerializer(instance=preferences, data=data, partial=True)



            if serializer.is_valid():
                serializer.save()
                token = CustomTokenObtainPairSerializer().get_token(user)
                return Response({'access': str(token.access_token)}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)


