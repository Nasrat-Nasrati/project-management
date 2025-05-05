from django.urls import path
from .views import SignupView
from .views import ActivateAccountView
from rest_framework_simplejwt import views as jwt_views
from .views import CustomLoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/', ActivateAccountView.as_view(), name='activate_account'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Built-in login view
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Re
    path('login/', CustomLoginView.as_view(), name='custom_login'),  # Use custom login view
]

