from apps.accounts.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class UserService:
    
    def __init__(self, user=None) -> None:
        self.user = user
        
    def GetTokenForUser(self):
        
        refresh=RefreshToken.for_user(self.user).access_token
        self.user.token = refresh
        self.user.save()
        
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    
    def CreateUser(self, email, password, **kwargs):
        try:
            # instance = self.Meta.model(**kwargs)
            self.user = User(email=email, **kwargs)

            if password is not None:
                self.user.set_password(password)
            
            self.user.is_active=True
            self.user.save()
        
        except IntegrityError as err:
            raise serializers.ValidationError(
                {"email": ["this user already exist"]}
            )
        self.user.refresh_from_db()
        token = self.GetTokenForUser()
        return self.user, token