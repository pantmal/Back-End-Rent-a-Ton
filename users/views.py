from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer

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