from rest_framework import serializers
from apps.certificates.models import Certificate
from apps.utils.services.tasks import generate_code
from apps.abattoirs.models import Abattoir

class IssueCertificateSerializer(serializers.ModelSerializer):
    
    #insert issuedBy, code from the code
    
    class Meta:
        fields = ['abattoir']
        model = Certificate
        
    def create(self, validated_data):
        user = self.request.user
        abattoir_id = validated_data['abattoir']
        try:
            abattoir = Abattoir.objects.get(id = abattoir_id)
            code = generate_code()
            certificate = Certificate.objects.create(
                abattoir = abattoir,
                code = code,
                issuedBy = user,
                
            )
        except Abattoir.DoesNotExist:
            raise serializers.ValidationError()
        
        return super().create(validated_data)