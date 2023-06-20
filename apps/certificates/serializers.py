from rest_framework import serializers
from apps.certificates.models import Certificate
from apps.utils.services.tasks import generate_code
from apps.abattoirs.models import Abattoir

class IssueCertificateSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        fields = ['abattoir', 'animalSpecie', 'typeOfParts', 'numberOfParts', 'dispatchedTo', 'serialNumberOfCarcass']
        model = Certificate
        
    def create(self, validated_data):
        user = self.request.user
        abattoir_id = validated_data['abattoir']
        try:
            abattoir = Abattoir.objects.get(id = abattoir_id)
            code = generate_code()
            Certificate.objects.create(
                abattoir = abattoir,
                code = code,
                issuedBy = user,
                
            )
        except Abattoir.DoesNotExist:
            raise serializers.ValidationError({'abattoir':f'abattoir with this id {abattoir_id} does not exist'})
        
        return super().create(validated_data)
    
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Certificate