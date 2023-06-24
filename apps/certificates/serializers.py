from rest_framework import serializers
from apps.certificates.models import Certificate
from apps.utils.services.tasks import generate_code
from apps.abattoirs.models import Abattoir
from apps.accounts.models import User

class IssueCertificateSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Certificate
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        # fields = ['id']
        exclude = ('user_permissions', 'groups', 'is_staff', 'is_admin', 'password', 'last_login', 'is_superuser', 'account_verified', 'account_verified_at', 'is_active', 'is_identity_verified')
        model = User
    
class CertificateSerializer(serializers.ModelSerializer):
    # issuedBy = UserSerializer()
    # issuedBy = serializers.SerializerMethodField()
    
    class Meta:
        fields = ['abattoir', 'animalSpecie', 'typeOfParts', 'numberOfParts', 'dispatchedTo', 'serialNumberOfCarcass', 'code', 'beefWeightInKg', 'issuedBy']
        model = Certificate
        extra_kwargs = {
            "code" : {
                    "read_only":True
                }
        }
        
    # def get_issuedBy(self, obj):
    #     return obj.issuedBy.id
    
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