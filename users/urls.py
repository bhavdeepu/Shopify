from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet
from django.urls import re_path

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls))

]