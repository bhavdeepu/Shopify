from django.urls import path, include
from rest_framework import routers
from client.views import ClientTenan

router = routers.DefaultRouter()
router.register(r'register', ClientTenan, basename='ClientTenan')


urlpatterns = [
    path('', include(router.urls)),
]