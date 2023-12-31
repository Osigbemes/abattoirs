from rest_framework import serializers
from apps.accounts.models import User
from apps.common.responses import CustomSuccessResponse, CustomErrorResponse
from apps.common.serializers import BaseModelSerializer
from rest_framework.response import Response
from django.contrib.auth.models import ContentType, Permission

class CreateUserSerializer(BaseModelSerializer):
    user_permissions = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = '__all__' #['permissions']
        extra_kwargs = {
            "password" : {
                    "write_only":True
                }
        }
        
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        if len(phone_number) < 11 or len(phone_number) > 11:
            raise serializers.ValidationError({'Phone number':'Phone number is invalid!'})
        return super().validate(attrs)
    
    def get_groups(self, obj):
        return [groups.name for groups in obj.groups.all()]
    
    def get_user_permissions(self, obj):
        group_permissions = []
        groups = obj.groups.all()
        if groups is not None:
            group_permissions.extend([perm.codename for perm in obj.user_permissions.all()])
            for group in groups:
                permissions = group.permissions.all()
                group_permissions.extend([permission.codename for permission in permissions])
            return group_permissions
        return [perm.codename for perm in obj.user_permissions.all()]
    
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def validate_email(self, value):
        return value.lower()


class LoginSerializer(EmailSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(required=True)
    
class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    
    class Meta:
        extra_kwargs = {
            "id" : {
                    "read_only":True
                }
        }
        
    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance
    
class PermissionSerializer(serializers.ModelSerializer):
    permissionId = serializers.IntegerField(required=False)
    userId = serializers.UUIDField(required = False)
    ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)
    
    class Meta:
        model = Permission
        fields = '__all__'
        
    
class ContentTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContentType
        fields = '__all__'
    