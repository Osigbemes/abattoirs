from rest_framework import serializers
from apps.certificates.models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = 