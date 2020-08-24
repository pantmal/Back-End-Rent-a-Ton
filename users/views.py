from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *
from permissions import *

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
    
        permission_classes = []
        if self.action == 'list' or self.action == 'retrieve' or self.action=='create':
            permission_classes = [AllowAny]
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser|IsAuthenticated]
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
    
        permission_classes = [IsHostUser|IsRenterUser]
        return [permission() for permission in permission_classes]



class GetUserByName(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):

        name = request.data['username']

        case = CustomUser.objects.filter(username=name).exists()

        if case == True:
            user = CustomUser.objects.get(username=name)
            userSerializer = UserSerializer(user)
            return Response(userSerializer.data)
        else:
            return Response('not found')

class GetMessages(APIView):

    permission_classes = [IsHostUser|IsRenterUser]

    def post(self, request, format=None):

        msg_type = request.data['type']        
        user_id = request.data['id']

        if msg_type == 'sent':
            case = Message.objects.filter(sender=user_id).exists()
            if case == True:
                messages = Message.objects.filter(sender=user_id)
                msgs_to_return = messages
                msg_Serializer = MessageSerializer(msgs_to_return, many=True)
                return Response(msg_Serializer.data)
            else:
                return Response('not found')
        elif msg_type == 'rec':
            case = Message.objects.filter(receiver=user_id).exists()
            if case == True:
                messages = Message.objects.filter(receiver=user_id)
                msgs_to_return = messages
                msg_Serializer = MessageSerializer(msgs_to_return, many=True)
                return Response(msg_Serializer.data)
            else:
                return Response('not found')


class approveUser(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        
        response_act = request.data['activation']

        response_id = request.data['ID']
        user = CustomUser.objects.get(pk=response_id)

        if user.is_host == True:
            user.approved = response_act
        
        user.save()

        return Response(status = status.HTTP_200_OK)