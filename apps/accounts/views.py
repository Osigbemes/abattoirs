from django.shortcuts import render
from rest_framework.generics import APIView
from accounts.models import User
from accounts.ser import UserSerializer

class GeneralClassView(APIView):
    queryset = User
    
