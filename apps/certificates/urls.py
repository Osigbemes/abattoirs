from django.urls import path
from rest_framework import routers
from apps.certificates.views import *

urlpatterns = [
   
]

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", CertificateViewSet)

urlpatterns += router.urls