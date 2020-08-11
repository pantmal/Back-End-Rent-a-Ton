from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

import datetime

# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class RoomRatingViewSet(viewsets.ModelViewSet):
    queryset = RoomRating.objects.all()
    serializer_class = RoomRatingSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class HostRatingViewSet(viewsets.ModelViewSet):
    queryset = HostRating.objects.all()
    serializer_class = HostRatingSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]                        

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]        

class ClickedItemViewSet(viewsets.ModelViewSet):
    queryset = ClickedItem.objects.all()
    serializer_class = ClickedItemSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]        


class SearchRooms(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        parameters = request.data.keys()
        
        rooms = Room.objects.all()

        rooms_to_return = []

        date_check = False
        hood_check = False
        loc_check = False
        ppl_check = False

        for room in rooms:
            if room.reserved == False:
                request_s_date = request.data['s_date']
                request_s_date = datetime.datetime.strptime(request_s_date, "%Y-%m-%d").date()

                request_e_date = request.data['e_date']
                request_e_date = datetime.datetime.strptime(request_e_date, "%Y-%m-%d").date()
                
                if room.start_date <= request_s_date <= room.end_date:
                    if room.start_date <= request_e_date <= room.end_date:
                        date_check = True

            if date_check == False:
                continue

            if room.neighborhood == request.data['hood']:
                hood_check = True

            if hood_check == False:
                continue
            
            if request.data['city'] in room.street:
                if request.data['country'] in room.street:
                    loc_check = True

            if loc_check == False:
                continue

            request_ppl = int(request.data['people'])
            if request_ppl <= room.max_people:
                ppl_check = True
            
            if ppl_check == False:
                continue

            if date_check == True and hood_check == True and loc_check == True and ppl_check == True:
                rooms_to_return.append(room)

            print(rooms_to_return)
        
        if not rooms_to_return:
            return Response('not found')
        else:
            roomSerializer = RoomSerializer(rooms_to_return, many=True)
            return Response(roomSerializer.data)