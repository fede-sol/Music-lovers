from django.shortcuts import render
from business.models import Event, Business
from business.serializers import BusinessPhotoSerializer, BusinessSerializer, EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateBusinessView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            if user.user_type != 1:
                return Response({
                    'error': 'No tiene permisos para crear eventos'},
                    status=status.HTTP_403_FORBIDDEN
                )
            existing_commerce = Business.objects.filter(user=user).exists()
            if existing_commerce:
                return Response({
                    'error': 'El usuario ya posee un negocio asignado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddImageBusinessView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if user.user_type == 1:

            try:
                business = Business.objects.get(user=user)
            except Business.DoesNotExist:
                return Response({'error': 'El usuario no posee un negocio asignado'}, status=status.HTTP_404_NOT_FOUND)

            request.data._mutable = True
            request.data['business'] = business.id

            serializer = BusinessPhotoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)

class CreateEventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.user_type == 1:

            try:
                business = Business.objects.get(user=user)
            except Business.DoesNotExist:
                return Response({'error': 'El usuario no posee un negocio asignado'}, status=status.HTTP_404_NOT_FOUND)

            request.data._mutable = True
            request.data['business'] = business.id

            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No tiene permisos para crear eventos'}, status=status.HTTP_403_FORBIDDEN)


class ModifyEventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id_event):
        user = request.user
        id_event = self.kwargs['id_event']

        try:
            event = Event.objects.get(id=id_event)
        except Event.DoesNotExist:
            return Response({'error': 'El evento no existe'}, status=status.HTTP_404_NOT_FOUND)

        if user == event.business.user:
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No tiene permisos para modificar este evento'}, status=status.HTTP_403_FORBIDDEN)


