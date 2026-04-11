from django.contrib import admin
from django.urls import path,include
from game.views.getinfo import InfoView
from game.views.register import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from game.views.test import index
urlpatterns = [
    path('',index,name="test"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/getinfo/',InfoView.as_view(),name="user_getinfo"),
    path('api/user/register/',RegisterView.as_view(),name="user_register")
]