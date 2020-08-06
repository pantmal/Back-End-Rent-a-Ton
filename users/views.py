from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
    
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class approveUser(APIView):

    permissions = [AllowAny]

    #@csrf_exempt #this SHOULD be temp
    def post(self, request, format=None):
        response_id = request.data['ID']
        response_act = request.data['activation']

        user = CustomUser.objects.get(pk=response_id)
        user.approved = response_act
        
        user.save()

        return Response(status = status.HTTP_200_OK)