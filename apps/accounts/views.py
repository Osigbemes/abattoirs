from rest_framework.views import APIView
from rest_framework import generics
from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from rest_framework.response import Response

class GeneralClassView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
