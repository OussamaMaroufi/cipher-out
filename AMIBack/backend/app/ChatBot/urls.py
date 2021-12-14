from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('', ChatViewSet, basename='chats')
router.register('messages/', MessageViewSet, basename='messages')

urlpatterns = [
    path('chats/', include(router.urls)),
    url('sendmsg/', sendMessage),
]
