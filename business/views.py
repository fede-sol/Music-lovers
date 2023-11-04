from business.models import BusinessComment, Event, Business, EventComment
from business.serializers import BusinessCommentSerializer, BusinessPhotoSerializer, BusinessSerializer, EventCommentSerializer, EventPhotoSerializer, EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ml_auth.serializers import CustomTokenObtainPairSerializer
from django.db.models import Q


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


class ModifyBusinessView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def put(self, request):
            user = request.user

            if user.user_type == 1:

                try:
                    business = Business.objects.get(user=user)
                except Business.DoesNotExist:
                    return Response({'error': 'El usuario no posee un negocio asignado'}, status=status.HTTP_404_NOT_FOUND)

                request.data._mutable = True

                if 'logo' not in request.data:
                    request.data['logo'] = business.logo
                if 'banner' not in request.data:
                    request.data['banner'] = business.banner


                serializer = BusinessSerializer(business, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    token = CustomTokenObtainPairSerializer().get_token(user)
                    return Response({'access': str(token.access_token)}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)

class BusinessView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            business = Business.objects.get(user=user)
        except Business.DoesNotExist:
            return Response({'error': 'El negocio no existe'}, status=status.HTTP_404_NOT_FOUND)

        serialized_business = BusinessSerializer(business)


        return Response(serialized_business.data, status=status.HTTP_200_OK)


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

            if 'banner' not in request.data:
                request.data['banner'] = event.banner

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


class FilterEventsView(APIView):

    def get(self, request):
        user = request.user

        title = request.query_params.get('title', None)
        genre = self.request.query_params.getlist('genre', [])
        address = request.query_params.get('address', None)
        neighborhood = request.query_params.get('neighborhood', None)
        city = request.query_params.get('city', None)
        artist = request.query_params.get('artist', None)
        maxprice = request.query_params.get('maxprice', None)
        minprice = request.query_params.get('minprice', None)
        maxdate = request.query_params.get('maxdate', None)
        mindate = request.query_params.get('mindate', None)

        events = Event.objects.all()

        if title:
            events = events.filter(title__icontains=title)
        if genre:
            query = Q()
            for g in genre:
                query = query | Q(genre__icontains=g)
            events = events.filter(query)
        if address:
            events = events.filter(address__icontains=address)
        if neighborhood:
            events = events.filter(neighborhood__icontains=neighborhood)
        if city:
            events = events.filter(city__icontains=city)
        if artist:
            events = events.filter(artist__icontains=artist)
        if maxprice:
            events = events.filter(price__lte=maxprice)
        if minprice:
            events = events.filter(price__gte=minprice)
        if maxdate:
            events = events.filter(datetime__date__lte=maxdate)
        if mindate:
            events = events.filter(datetime__date__gte=mindate)


        serialized_events = EventSerializer(events, many=True)
        return Response(serialized_events.data, status=status.HTTP_200_OK)


class FilterBusinessView(APIView):

    def get(self, request):
        user = request.user

        name = request.query_params.get('name', None)
        address = request.query_params.get('address', None)
        neighborhood = request.query_params.get('neighborhood', None)
        city = request.query_params.get('city', None)

        businesses = Business.objects.all()

        if name:
            businesses = businesses.filter(name__icontains=name)
        if address:
            businesses = businesses.filter(address__icontains=address)
        if neighborhood:
            businesses = businesses.filter(neighborhood__icontains=neighborhood)
        if city:
            businesses = businesses.filter(city__icontains=city)

        serialized_businesses = BusinessSerializer(businesses, many=True)
        return Response(serialized_businesses.data, status=status.HTTP_200_OK)



class GetEventView(APIView):

    def get(self, request):
        user = request.user

        try:
            event = Event.objects.get(id=request.query_params.get('id', None))
        except Event.DoesNotExist:
            return Response({'error': 'El evento no existe'}, status=status.HTTP_404_NOT_FOUND)


        comments = EventComment.objects.filter(event=event)

        serialized_event = EventSerializer(event)
        serialized_comments = EventCommentSerializer(comments, many=True)

        return Response({'event':serialized_event.data,'comments':serialized_comments.data}, status=status.HTTP_200_OK)


class GetBusinessView(APIView):

    def get(self, request):
        user = request.user

        try:
            business = Business.objects.get(id=request.query_params.get('id', None))
        except Business.DoesNotExist:
            return Response({'error': 'El negocio no existe'}, status=status.HTTP_404_NOT_FOUND)


        comments = BusinessComment.objects.filter(business=business)

        serialized_business = BusinessSerializer(business)
        serialized_comments = BusinessCommentSerializer(comments, many=True)

        return Response({'business':serialized_business.data,'comments':serialized_comments.data}, status=status.HTTP_200_OK)