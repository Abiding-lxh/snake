from django.contrib import admin
from django.urls import path,include
from game.views.getinfo import InfoView
from game.views.register import RegisterView

from game.views.botAdd import BotAddView
from game.views.botRemove import BotRemoveView
from game.views.botUpdate import BotUpdateView
from game.views.botList import BotListView
from game.views.getRecord import getRecordView
from game.views.ranklist import rankListView

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
    path('api/user/register/',RegisterView.as_view(),name="user_register"),
    path('api/bot/add/',BotAddView.as_view(),name="bot_add"),
    path('api/bot/remove/',BotRemoveView.as_view(),name="bot_remove"),
    path('api/bot/update/',BotUpdateView.as_view(),name="bot_update"),
    path('api/bot/list/',BotListView.as_view(),name="bot_list"),
    path('api/getrecord/',getRecordView.as_view(),name="get_record"),
    path('api/ranklist/',rankListView.as_view(),name="ranklist")
]