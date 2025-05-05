
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Activation,UserProfile


User = get_user_model()  # به جای import مستقیم از get_user_model استفاده کن (چون User را Extend کردی)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_picture']


class SignupSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 
            'first_name', 'last_name', 
            'profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        # ایجاد Activation Code
        Activation.objects.create(user=user)

        # ساختن پروفایل همراه با عکس
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)

        return user

    # serializers.py

