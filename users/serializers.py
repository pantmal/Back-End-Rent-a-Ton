from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'telephone', 'approved', 'is_host', 'is_renter','picture']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        #password = validated_data.pop('password')
        #instance.set_password(password)
        return CustomUser.objects.create_user(**validated_data)

    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.text = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.is_host = validated_data.get('is_host', instance.is_host)
        instance.is_renter = validated_data.get('is_renter', instance.is_renter)
        instance.picture = validated_data.get('picture', instance.picture)

        #password = ''
        #if(validated_data.pop('password')):
        password = validated_data.pop('password')
        instance.set_password(password)

        instance.save()
        return instance
    