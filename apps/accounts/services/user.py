from apps.accounts.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from apps.accounts.services.tasks import send_email
from apps.common.responses import SerializerCustomErrorResponse

class UserService:
    
    def __init__(self, user=None) -> None:
        self.user = user
        
    def GetTokenForUser(self):
        
        refresh=RefreshToken.for_user(self.user)
        last_login = timezone.now() + timezone.timedelta(hours=1)
        self.user.last_login = last_login
        self.user.save()
        
        refresh['firstname']=self.user.firstname
        refresh['email']=self.user.email
        
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    
    @transaction.atomic
    def CreateUser(self, email, password, **kwargs):
        try:
            # instance = self.Meta.model(**kwargs)
            kwargs.pop('groups', None)
            self.user = User(email=email, **kwargs)

            if password is not None:
                self.user.set_password(password)
            
            self.user.is_active=True
            # self.user.groups.set(groups)
            self.user.save()
        
        except IntegrityError as err:
            raise serializers.ValidationError(
                {"email": ["this user already exist"]}
            )
        
        send_email(email, "Welcome to protein tech", "click this link to verify your account", " ")
        self.user.refresh_from_db()
        token = self.GetTokenForUser()
        return self.user, token
    
    @transaction.atomic
    def CreateGroup(self, name):
        if not Group.objects.filter(name=name).exists():
            group = Group.objects.create(name=name)
            return group
        raise serializers.ValidationError(
            {
                {"name": ["this group name already exist"]}
            }
        )
        
    @transaction.atomic
    def create_permission_for_user(self, userId, permissionId):
        try:
            user = User.objects.get(id=userId)
            permission = Permission.objects.get(id=permissionId)
            if user.has_perm(permission.codename):
                raise serializers.ValidationError({
                    "User":f"user already exist with this permission '{permission.codename}'"
                })
            user.user_permissions.add(permission)
            user.save()
            return permission
            
        except User.DoesNotExist:
            SerializerCustomErrorResponse(message="user does not exist")
            
        except Permission.DoesNotExist:
            SerializerCustomErrorResponse(message=f"Permission with this id {permissionId} does not exist")
        except IntegrityError:
            SerializerCustomErrorResponse(message="Unable to create permission")
            
    @transaction.atomic
    def create_permissions_for_user(self, userId, ids):
        try:
            user = User.objects.get(id=userId)
            
            user.user_permissions.set(ids)
            user.save()
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "User":f"user with this id {userId} does not exist"
            })
        except Permission.DoesNotExist:
            raise serializers.ValidationError({
                "Permission" : "Permission does not exist"
            })
        except IntegrityError:
            raise serializers.ValidationError({
                "IntegrityError":"Unable to create permission"
            })
            
    def Login(self, email, password):
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                {"email": ["invalid login details"]}
            )
        if not user.is_active:
            raise serializers.ValidationError(
                {"email": ["this user is currently not active. kindly contact support"]}
            )
        self.user = user
        token = self.GetTokenForUser()
        
        return self.user, token
        
    def logout(self, token):
        token = RefreshToken(token)
        token.blacklist()
        