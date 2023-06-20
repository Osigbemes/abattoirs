from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from apps.certificates.serializers import IssueCertificateSerializer, CertificateSerializer
from apps.certificates.models import Certificate
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from apps.utils.services.certificate import generate_certificate
from rest_framework.response import Response
from apps.common.responses import CustomErrorResponse, CustomSuccessResponse

class IssueCertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IssueCertificateSerializer

    def list(self, request, *args, **kwargs):
        raise NotFound()
    
    def get(self, request, *args, **kwargs):
        raise NotFound()
    
    def create(self, request, *args, **kwargs):
        raise NotFound()
    
    @action(
    methods=["get"],
    detail=False,
    url_path="download_certificate/<int:pk>",
    permission_classes=[IsAuthenticated]
    )
    def get_certificate(self, request, pk):
        user = request.user
        try:
            certificate = Certificate.objects.get(id=pk)
            abattoir = {
                'abattoir':certificate.abattoir,
                'issuedBy':certificate.issuedBy,
                'beefWeightInKg':certificate.beefWeightInKg,
                'animalSpecie':certificate.animalSpecie,
                'dispatchedTo':certificate.dispatchedTo
            }
        except Certificate.DoesNotExist:
            return CustomErrorResponse(data={}, message="Certificate does not exist")
        
        certificate_response = generate_certificate(request, abattoir)
        return HttpResponse(certificate_response, content_type='application/pdf')
    
    
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CertificateSerializer
    
    def create(self, request, *args, **kwargs):
        raise NotFound()