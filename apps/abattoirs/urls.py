from django.urls import path
from rest_framework import routers
from apps.abattoirs.views import *

urlpatterns = [
   
]

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", AbattoirViewSet)

urlpatterns += router.urls