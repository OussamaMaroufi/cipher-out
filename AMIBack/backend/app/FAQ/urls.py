from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('', FAQViewSet, basename='faq')


urlpatterns = [
    path('faq/', include(router.urls)),
]
