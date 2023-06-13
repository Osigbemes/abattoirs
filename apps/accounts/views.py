from rest_framework import generics
from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer

class GeneralClassView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
