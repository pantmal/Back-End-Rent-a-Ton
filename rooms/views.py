from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Avg
from .models import *
from .serializers import *
from users.models import *

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

class SearchedItemViewSet(viewsets.ModelViewSet):
    queryset = SearchedItem.objects.all()
    serializer_class = SearchedItemSerializer

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

        if 'host_id' in parameters:

            rooms = rooms.filter(host_id=request.data['host_id'])
            rooms_to_return = rooms
            if not rooms_to_return:
                return Response('not found')
            else:
                roomSerializer = RoomSerializer(rooms_to_return, many=True)
                return Response(roomSerializer.data)

        if 'renter_id' in parameters:

            reservations = Reservation.objects.filter(renter_id_res=request.data['renter_id'])

            roomss = []
            for res in reservations:
                roomss.append(res.room_id_res)

            rooms_to_return = roomss
            if not rooms_to_return:
                return Response('not found')
            else:
                roomSerializer = RoomSerializer(rooms_to_return, many=True)
                return Response(roomSerializer.data)

        print(request.data['user_id'])
        rooms = rooms.exclude(host_id=request.data['user_id'])

        rooms = rooms.filter(neighborhood=request.data['hood'])
        rooms = rooms.filter(city=request.data['city'])
        rooms = rooms.filter(country=request.data['country'])

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


        request_ppl = int(request.data['people'])
        rooms = rooms.filter(max_people__gte=request_ppl)

        date_check = False
        
        request_s_date = request.data['s_date']
        request_s_date = datetime.datetime.strptime(request_s_date, "%Y-%m-%d").date()

        request_e_date = request.data['e_date']
        request_e_date = datetime.datetime.strptime(request_e_date, "%Y-%m-%d").date()
        case = rooms.filter(start_date__lte=request_s_date, end_date__gte=request_e_date).exists()
        
        if case==True:
            rooms = rooms.filter(start_date__lte=request_s_date, end_date__gte=request_e_date)
            
            for room in rooms:
                case_1 = Reservation.objects.filter(room_id_res=room.id, start_date__lte=request_s_date, end_date__gte=request_s_date).exists()
                if case_1:
                    rooms = rooms.exclude(pk=room.id)    

                case_2 = Reservation.objects.filter(room_id_res=room.id, start_date__lte=request_e_date, end_date__gte=request_e_date).exists()
                if case_2:
                    rooms = rooms.exclude(pk=room.id)    

                case_3 = Reservation.objects.filter(room_id_res=room.id, start_date__gte=request_s_date, end_date__lte=request_e_date).exists()
                if case_3:
                    rooms = rooms.exclude(pk=room.id)    
            

        rooms_to_return = []
        final_rooms = []
        
        if 'max_price' in parameters:
            if 'max_price' != '':

                for room in rooms:
                
                    total_price = room.price + ((request_ppl-1) * room.price_per_person)
                    request_price = int(request.data['max_price']) #CHANGE TO FLOAT SOMETIME
                    if total_price <= request_price:
                        final_rooms.append(room)    
            else:
                final_rooms = rooms    
        else:
            final_rooms = rooms
        
    
        rooms_to_return = final_rooms
        print(rooms_to_return)
        

        if not rooms_to_return:
            return Response('not found')
        else:
            roomSerializer = RoomSerializer(rooms_to_return, many=True)
            return Response(roomSerializer.data)

class GetImages(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        parameters = request.data.keys()
        
        images = RoomImage.objects.all()

        imgs_to_return = []
        
        images = images.filter(room_id_img=request.data['room_id_img'])
        imgs_to_return = images
        if not imgs_to_return:
            return Response('not found')
        else:
            roomImageSerializer = RoomImageSerializer(imgs_to_return, many=True)
            return Response(roomImageSerializer.data)

class AddSearchesClicks(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        parameters = request.data.keys()
        
        searches = []
        clicks = []
        already_there = False
        if 'search' in parameters:
            searches = SearchedItem.objects.all()
            case1 = searches.filter(room_id_search=request.data['room_id_search']).exists()
            case2 = searches.filter(renter_id_search=request.data['renter_id_search']).exists()
            if case1 and case2:
                already_there = True
        if 'click' in parameters:
            clicks = ClickedItem.objects.all()
            case1 = clicks.filter(room_id_click=request.data['room_id_click']).exists()
            case2 = clicks.filter(renter_id_click=request.data['renter_id_click']).exists()
            if case1 and case2:
                already_there = True

        if already_there == False:
            if 'search' in parameters:
                search = SearchedItem(room_id_search=Room.objects.get(pk=request.data['room_id_search']),renter_id_search=CustomUser.objects.get(pk=request.data['renter_id_search']) )
                search.save()
            if 'click' in parameters:
                click = ClickedItem(room_id_click=Room.objects.get(pk=request.data['room_id_click']),renter_id_click=CustomUser.objects.get(pk=request.data['renter_id_click']))
                click.save()

        return Response('ok')
        
class ReservationCheck(APIView):       

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        parameters = request.data.keys()    
       
        check_in = request.data['start_date'] 
        check_out = request.data['end_date']

        # check wether the dates are valid
        # case 1: a room is booked before the check_in date, and checks out after the requested check_in date
        case_1 = Reservation.objects.filter(room_id_res=request.data['room_id'], start_date__lte=check_in, end_date__gte=check_in).exists()

        # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
        case_2 = Reservation.objects.filter(room_id_res=request.data['room_id'], start_date__lte=check_out, end_date__gte=check_out).exists()
        
        case_3 = Reservation.objects.filter(room_id_res=request.data['room_id'], start_date__gte=check_in, end_date__lte=check_out).exists()

        if case_1 or case_2 or case_3:
            return Response('taken')
        else:
            return Response('free')

class RatingCheck(APIView):       

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        parameters = request.data.keys()    

        room_id = request.data['room_id']
        user_id = request.data['user_id']
        date_now = request.data['date_now']
        
        case = Reservation.objects.filter(room_id_res=room_id, renter_id_res=user_id, end_date__lt=date_now).exists()

        if case:
            return Response('free')
        else:
            return Response('bounded')

class RatingCount(APIView):       

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        parameters = request.data.keys()                

        room_id = ''
        if 'room' in parameters:
            room_id = request.data['room_id']

            count = len(RoomRating.objects.filter(room_id_rate=room_id))
            avg = RoomRating.objects.filter(room_id_rate=room_id).aggregate(Avg('rating'))

            print(count)
            print(avg)

            return Response({'count':count,'avg':avg})

        host_id = ''
        if 'host' in parameters:
            host_id = request.data['host_id']

            count = len(HostRating.objects.filter(host_id_hostRate=host_id))
            avg = HostRating.objects.filter(host_id_hostRate=host_id).aggregate(Avg('rating'))

            print(count)
            print(avg)

            return Response({'count':count,'avg':avg})

        return Response('something went wrong')