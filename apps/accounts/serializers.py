from rest_framework import serializers
from apps.accounts.models import User
from apps.common.responses import CustomSuccessResponse, CustomErrorResponse

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            "password" : {
                    "write_only":True
                }
        }
        
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        if len(phone_number) < 11 or len(phone_number) > 11:
            return CustomErrorResponse({'Phone number':'Phone number is invalid!'})
        return super().validate(attrs)