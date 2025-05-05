
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User
# from django.core.mail import send_mail
# import uuid  # to generate activation code
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# import random

# class SignupView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')
#         first_name = request.data.get('first_name', '')
#         last_name = request.data.get('last_name', '')

#         if User.objects.filter(username=username).exists():
#             return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             is_active=False  # مهم! کاربر غیرفعال است تا زمانی که ایمیل را تایید کند
#         )

#         # تولید کد فعال‌سازی ساده
#         activation_code = str(random.randint(100000, 999999))
#         user.profile.activation_code = activation_code
#         user.profile.save()

#         # ارسال ایمیل
#         send_mail(
#             'Activate your account',
#             f'Your activation code is: {activation_code}',
#             'from@example.com',
#             [email],
#             fail_silently=False,
#         )

#         return Response({'message': 'Signup successful. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)




# class ActivateAccountView(APIView):
#     def post(self, request):
#         activation_code = request.data.get('activation_code')

#         if not activation_code:
#             return Response({'error': 'Activation code is required'}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if there's a user with the provided activation code
#         try:
#             user = User.objects.get(activation_code=activation_code)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid activation code'}, status=status.HTTP_400_BAD_REQUEST)

#         # If the user is already active, return an error
#         if user.is_active:
#             return Response({'error': 'Account already activated'}, status=status.HTTP_400_BAD_REQUEST)

#         # Mark the user as active
#         user.is_active = True
#         user.activation_code = None  # Clear the activation code after activation
#         user.save()

#         return Response({'message': 'Account successfully activated!'}, status=status.HTTP_200_OK)




# class CustomLoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#         # Authenticate user
#         user = authenticate(request, username=username, password=password)

#         if user is None:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

#         if not user.is_active:
#             return Response({'error': 'Account is not active'}, status=status.HTTP_400_BAD_REQUEST)

#         # Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         return Response({
#             'access': access_token,
#             'refresh': str(refresh),
#         }, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import random

class SignupView(APIView):
    permission_classes = [AllowAny]  # 👈 Allow anyone to signup

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False  # User inactive until they activate
        )

        # Generate and save activation code
        activation_code = str(random.randint(100000, 999999))
        user.profile.activation_code = activation_code
        user.profile.save()

        # Send email
        send_mail(
            'Activate your account',
            f'Your activation code is: {activation_code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Signup successful. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]  # 👈 Allow anyone to activate account

    def post(self, request):
        activation_code = request.data.get('activation_code')

        if not activation_code:
            return Response({'error': 'Activation code is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the user by checking profile activation_code
        try:
            user_profile = User.objects.get(profile__activation_code=activation_code).profile
            user = user_profile.user
        except User.DoesNotExist:
            return Response({'error': 'Invalid activation code'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'error': 'Account already activated'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate the user
        user.is_active = True
        user.save()

        # Clear activation code
        user_profile.activation_code = ''
        user_profile.save()

        return Response({'message': 'Account successfully activated!'}, status=status.HTTP_200_OK)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]  # 👈 Allow anyone to login

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'error': 'Account is not active'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token,
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
