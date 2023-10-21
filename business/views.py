from business.models import Event, Business
from business.serializers import BusinessPhotoSerializer, BusinessSerializer, EventPhotoSerializer, EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from ml_auth.serializers import CustomTokenObtainPairSerializer


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
            token = CustomTokenObtainPairSerializer().get_token(user)
            return Response({'access': str(token.access_token)}, status=status.HTTP_201_CREATED)
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

class BusinessEventsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.user_type == 1:

            try:
                business = Business.objects.get(user=user)
            except Business.DoesNotExist:
                return Response({'error': 'El usuario no posee un negocio asignado'}, status=status.HTTP_404_NOT_FOUND)

            events = Event.objects.filter(business=business)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
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

    def put(self, request):
        user = request.user
        id_event = request.data['id']

        try:
            event = Event.objects.get(id=id_event)
        except Event.DoesNotExist:
            return Response({'error': 'El evento no existe'}, status=status.HTTP_404_NOT_FOUND)

        if user == event.business.user:
            request.data._mutable = True
            request.data['business'] = event.business.id
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No tiene permisos para modificar este evento'}, status=status.HTTP_403_FORBIDDEN)


class AddImageEventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.user_type == 1:

            try:
                business = Business.objects.get(user=user)
            except Business.DoesNotExist:
                return Response({'error': 'El usuario no posee un negocio asignado'}, status=status.HTTP_404_NOT_FOUND)


            try:
                if Event.objects.get(id=request.data['event']).business.user != user:
                    return Response({'error': 'El evento no pertenece a este negocio'}, status=status.HTTP_403_FORBIDDEN)
            except Event.DoesNotExist:
                return Response({'error': 'El evento no existe'}, status=status.HTTP_404_NOT_FOUND)


            serializer = EventPhotoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)

class DeleteEventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        if user.user_type == 1:

            try:
                business = Business.objects.get(user=user)
            except Business.DoesNotExist:
                return Response({'error': 'El usuario no posee un negocio asignado'}, status=status.HTTP_404_NOT_FOUND)


            try:
                events = Event.objects.filter(business=business)
                events.get(id=request.data['id']).delete()
            except Event.DoesNotExist:
                return Response({'error': 'El evento no existe'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message':'Evento eliminado exitosamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)

