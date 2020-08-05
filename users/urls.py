from django.urls import path, include
from .views import UserViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'userList', UserViewSet)

urlpatterns = [

    path(r'', include(router.urls)),
    path(r'authentication/', include('rest_auth.urls'))
]
