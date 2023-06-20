from rest_framework import serializers
from apps.certificates.models import Certificate
from apps.utils.services.tasks import generate_code
from apps.abattoirs.models import Abattoir

class IssueCertificateSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Certificate
    
class CertificateSerializer(serializers.ModelSerializer):
        
    class Meta:
        fields = ['abattoir', 'animalSpecie', 'typeOfParts', 'numberOfParts', 'dispatchedTo', 'serialNumberOfCarcass', 'code', 'beefWeightInKg']
        model = Certificate
        extra_kwargs = {
            "code" : {
                    "read_only":True
                }
        }
        
    def create(self, validated_data):
        user = self.context.get('request').user
        abattoir_id = validated_data['abattoir']
        try:
            abattoir = Abattoir.objects.get(id = abattoir_id.id)
            validated_data.pop('abattoir', None)
            code = generate_code()
            Certificate.objects.create(
                abattoir = abattoir,
                code = code,
                issuedBy = user.id,
                **validated_data
            )
        except Abattoir.DoesNotExist:
            raise serializers.ValidationError({'abattoir':f'abattoir with this id {abattoir_id} does not exist'})
        
        return super().create(validated_data)