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


        rooms = rooms.filter(neighborhood=request.data['hood'])

        if 'room_type' in parameters:
            if 'room_type' != '':
                if request.data['room_type'] == 'Private_room':
                    rooms = rooms.filter(room_type='Private room')
                if request.data['room_type'] == 'Shared_room':
                    rooms = rooms.filter(room_type='Shared room')
                if request.data['room_type'] == 'Entire_home/apt':
                    rooms = rooms.filter(room_type='Entire home/apt')

        
        if 'wifi' in parameters:
            if request.data['wifi'] == 'true':
                rooms = rooms.filter(has_wifi=True)

        if 'freezer' in parameters:
            if request.data['freezer'] == 'true':
                rooms = rooms.filter(has_freezer=True)

        if 'heating' in parameters:
            if request.data['heating'] == 'true':
                rooms = rooms.filter(has_heating=True)

        if 'kitchen' in parameters:
            if request.data['kitchen'] == 'true':
                rooms = rooms.filter(has_kitchen=True)

        if 'TV' in parameters:
            if request.data['TV'] == 'true':
                rooms = rooms.filter(has_TV=True)

        if 'parking' in parameters:
            if request.data['parking'] == 'true':
                rooms = rooms.filter(has_parking=True)

        if 'elevator' in parameters:
            if request.data['elevator'] == 'true':
                rooms = rooms.filter(has_elevator=True)

        date_check = False
        loc_check = False
        ppl_check = False
        price_check = False

        for room in rooms:
            request_ppl = int(request.data['people'])
            total_price = room.price + ((request_ppl-1) * room.price_per_person)

            if 'max_price' in parameters:
                if 'max_price' != '':
                    request_price = int(request.data['max_price']) #CHANGE TO FLOAT SOMETIME
                    if total_price <= request_price:
                        price_check = True
                    else:
                        price_check = False
                else:
                    price_check = True
            else:
                price_check = True

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

            
            if request.data['city'] in room.street:
                if request.data['country'] in room.street:
                    loc_check = True

            if loc_check == False:
                continue

            
            if request_ppl <= room.max_people:
                ppl_check = True
            
            if ppl_check == False:
                continue

            if date_check == True and loc_check == True and ppl_check == True and price_check == True:
                rooms_to_return.append(room)

            print(rooms_to_return)
        
        if not rooms_to_return:
            return Response('not found')
        else:
            roomSerializer = RoomSerializer(rooms_to_return, many=True)
            return Response(roomSerializer.data)