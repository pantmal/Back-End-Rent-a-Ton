from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):

    #inherited fields: first_name, last_name, password, is_staff 
   
    #username = models.CharField(unique = True, max_length=100)
    #email = models.EmailField('email add', unique=True)
    telephone = models.CharField(max_length=100)
    approved = models.BooleanField(default=True)
    is_host = models.BooleanField(default=False)
    is_renter = models.BooleanField(default=False)
    picture = models.FileField(upload_to='user_images',blank=True,null=True)
    secondary_id = models.IntegerField()

    #session_client = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    #location = models.PointField(null=True, blank=True)

#Check sometime: proper extend of user model
#class Profile(models.Model): 
#    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
