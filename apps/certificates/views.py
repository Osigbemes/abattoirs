from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from apps.certificates.serializers import IssueCertificateSerializer, CertificateSerializer
from apps.certificates.models import Certificate
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from apps.utils.services.certificate import generate_certificate, generate_certificate_for_abattoir
from rest_framework.response import Response

class IssueCertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IssueCertificateSerializer

    def list(self, request, *args, **kwargs):
        raise NotFound()
    
    def get(self, request, *args, **kwargs):
        raise NotFound()
    
    @action(
    methods=["post"],
    detail=False,
    url_path="download_certificate",
    permission_classes=[IsAuthenticated]
    )
    def get_certificate(self, request):
        user = request.user
        name = user.firstname
        certificate = generate_certificate(request)
        return HttpResponse(certificate, content_type='application/pdf')
    
    
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CertificateSerializer
    
    def create(self, request, *args, **kwargs):
        raise NotFound()