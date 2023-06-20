from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from apps.certificates.serializers import IssueCertificateSerializer
from apps.certificates.models import Certificate

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IssueCertificateSerializer
