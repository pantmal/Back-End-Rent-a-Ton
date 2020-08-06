from django.urls import path, include
from .views import UserViewSet
from rest_framework import routers

from users.views import *
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'userList', UserViewSet)

urlpatterns = [

    path(r'', include(router.urls)),
    path(r'authentication/', include('rest_auth.urls')),
    path('approveUser/', approveUser.as_view(), name='approve-user')
]
