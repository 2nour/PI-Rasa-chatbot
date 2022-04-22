from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    ]
