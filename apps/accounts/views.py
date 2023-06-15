from rest_framework.views import APIView
from rest_framework import generics, viewsets
from apps.accounts.models import User
from apps.accounts.serializers import CreateUserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from django.db import transaction
from apps.accounts.services.user import UserService

class GeneralClassView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = CreateUserSerializer(user)
        return Response(serializer.data)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        raise NotFound()

    def create(self, request, *args, **kwargs):
        raise NotFound()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    @action(
        methods=["post"],
        detail=False,
        url_path="create",
        permission_classes=[AllowAny],
    )
    def user_create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            user_service = UserService()
            user, token = user_service.CreateUser(
                **validated_data
            )

            data = {
                "access": token.get("access"),
                "refresh": token.get("refresh"),
                "user": self.get_serializer(user).data
            }

            return Response(data, status=201)
        
    @action(
    methods=["get"],
    detail=False,
    url_path="retrieve",
    permission_classes=[AllowAny]
    )
    def user_retrieve(self, request, *args, **kwargs):
        user = request.user
        data = self.get_serializer(user).data
        return Response(data)
    
    
