from django.contrib.gis.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Room(models.Model):

    PRIV = "PRIVATE ROOM"
    SHARE = "SHARED ROOM"
    ENTIRE = "ENTIRE HOUSE"
    
    ROOM_CHOICES = (
        (PRIV, "Private room"),
        (SHARE, "Shared room"),
        (ENTIRE, "Entire home/apt")
    )

    name = models.CharField(max_length=50, null=False)
    geolocation = models.PointField(null=False)
    street = models.CharField(max_length=100, null=False)
    neighborhood = models.CharField(max_length=50, null=False)
    transit = models.CharField(max_length=500, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    price = models.FloatField(null=False)
    price_per_person = models.FloatField(null=False)
    max_people = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    rep_photo = models.FileField(upload_to='room_images',blank=True,null=False)
    room_type = models.CharField(choices=ROOM_CHOICES, default=ENTIRE, max_length=20)
    has_wifi = models.BooleanField(default=False)
    has_heating = models.BooleanField(default=False)
    has_freezer = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    has_TV = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_living_room = models.BooleanField(default=False)
    square_feet = models.FloatField(null=False)
    description = models.TextField(max_length=2000, null=False)
    smoking = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    events = models.BooleanField(default=False)
    minimum_nights = models.IntegerField()
    host_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='host', on_delete=models.CASCADE, null=False)
    reserved = models.BooleanField(default=False)


class RoomImage(models.Model):

    room_id_img = models.ForeignKey(Room, related_name='room_img', on_delete=models.CASCADE, null=False)
    picture = models.FileField(upload_to='user_images',blank=True,null=True)

class RoomRating(models.Model):

    room_id_rate = models.ForeignKey(Room, related_name='room_rate', on_delete=models.CASCADE, null=False)
    renter_id_rate = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='renter_rate', on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(null=False)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])


class HostRating(models.Model):

    host_id_hostRate = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='host_hostRate', on_delete=models.CASCADE, null=False)
    renter_id_hostRate = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='renter_hostRate', on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(null=False)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

class Reservation(models.Model):

    room_id_res = models.ForeignKey(Room, related_name='room_res', on_delete=models.CASCADE, null=False)
    renter_id_res = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='renter_res', on_delete=models.CASCADE, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    price = models.FloatField(null=False)

class ClickedItem(models.Model):

    room_id_click = models.ForeignKey(Room, related_name='room_click', on_delete=models.CASCADE, null=False)
    renter_id_click = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='renter_click', on_delete=models.CASCADE, null=False)



