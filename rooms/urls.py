from django.urls import path, include
from .views import *
from rest_framework import routers

from rooms.views import *


router = routers.DefaultRouter()
router.register(r'roomList', RoomViewSet)
router.register(r'roomImages', RoomImageViewSet)
router.register(r'roomRatings', RoomRatingViewSet)
router.register(r'hostRatings', HostRatingViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'clickedItems', ClickedItemViewSet)

searchView = SearchRooms.as_view()

urlpatterns = [

    path(r'', include(router.urls)),
    path('search/', searchView, name='search-rooms')
] 