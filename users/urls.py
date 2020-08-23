from django.urls import path, include
from .views import UserViewSet
from rest_framework import routers

from users.views import *


router = routers.DefaultRouter()
router.register(r'userList', UserViewSet)
router.register(r'messageList', MessageViewSet)

approveUser_view = approveUser.as_view()
GetUserByName_view = GetUserByName.as_view()
getMessages_view = GetMessages.as_view()

urlpatterns = [

    path(r'', include(router.urls)),
    path(r'authentication/', include('rest_auth.urls')),
    path('getUserByName/', GetUserByName_view, name='get-user-by-name'),
    path('getMessages/', getMessages_view, name='get-messages'),
    path('approveUser/', approveUser_view, name='approve-user')

] 
