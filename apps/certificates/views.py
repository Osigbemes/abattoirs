from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from apps.certificates.serializers import IssueCertificateSerializer, CertificateSerializer
from apps.certificates.models import Certificate
from rest_framework.exceptions import NotFound

class IssueCertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IssueCertificateSerializer

    def list(self, request, *args, **kwargs):
        raise NotFound()
    
    def get(self, request, *args, **kwargs):
        raise NotFound()
    
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CertificateSerializer
    
    def create(self, request, *args, **kwargs):
        raise NotFound()