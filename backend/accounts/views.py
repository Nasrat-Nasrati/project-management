
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.core.mail import send_mail
import uuid  # to generate activation code
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Create user but set is_active=False
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Step 2: Generate activation code
        activation_code = str(uuid.uuid4())

        # Step 3: Save activation code to user (or separate model if you use one)
        user.activation_code = activation_code
        user.save()

        # ✅ Step 4: Send activation email here
        activation_link = f"http://localhost:8000/api/activate/{activation_code}/"

        send_mail(
            subject="Activate your account",
            message=f"Click the link to activate your account: {activation_link}",
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({'message': 'User created. Check your email to activate your account.'}, status=status.HTTP_201_CREATED)
    




class ActivateAccountView(APIView):
    def post(self, request):
        activation_code = request.data.get('activation_code')

        if not activation_code:
            return Response({'error': 'Activation code is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if there's a user with the provided activation code
        try:
            user = User.objects.get(activation_code=activation_code)
        except User.DoesNotExist:
            return Response({'error': 'Invalid activation code'}, status=status.HTTP_400_BAD_REQUEST)

        # If the user is already active, return an error
        if user.is_active:
            return Response({'error': 'Account already activated'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the user as active
        user.is_active = True
        user.activation_code = None  # Clear the activation code after activation
        user.save()

        return Response({'message': 'Account successfully activated!'}, status=status.HTTP_200_OK)




class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
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


