from django.shortcuts import render
from rest_framework import viewsets, generics
from apps.abattoirs.models import Abattoir
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from apps.abattoirs.serializers import AbattoirSerializer


class AbattoirViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Abattoir.objects.all()
    serializer_class = AbattoirSerializer
