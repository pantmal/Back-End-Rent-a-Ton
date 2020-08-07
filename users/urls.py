from django.urls import path, include
from .views import UserViewSet
from rest_framework import routers

from users.views import *


router = routers.DefaultRouter()
router.register(r'userList', UserViewSet)

approveUser_view = approveUser.as_view()

urlpatterns = [

    path(r'', include(router.urls)),
    path(r'authentication/', include('rest_auth.urls')),
    path('approveUser/', approveUser_view, name='approve-user')

] 
