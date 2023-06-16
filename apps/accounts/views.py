from rest_framework.views import APIView, status
from rest_framework import generics, viewsets, permissions, mixins
from apps.accounts.models import User
from apps.accounts.serializers import CreateUserSerializer, LoginSerializer, GroupSerializer, ContentTypeSerializer, PermissionSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from django.db import transaction
from apps.accounts.services.user import UserService
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView
from apps.common.responses import CustomErrorResponse, CustomSuccessResponse
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer, TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.models import Group, Permission, ContentType
from apps.accounts.permissions import CustomPermisions   

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

            return CustomSuccessResponse(data, status=201)
        
    @action(
    methods=["post"],
    detail=False,
    url_path="login",
    permission_classes=[AllowAny]
    )
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email= validated_data.get('email')
        password = validated_data.get('password')
        user_service = UserService()
        user, token = user_service.Login(email, password)
            
        data = {
            "access": token.get("access"),
            "refresh": token.get("refresh"),
            "user": self.get_serializer(user).data
        }
        return CustomSuccessResponse(data)    
    
    @action(
    methods=["post"],
    detail=False,
    url_path="logout",
    permission_classes=[IsAuthenticated]
    )
    def logout(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            user_service = UserService()
            user_service.logout(refresh_token)
            return Response("You are logged out", status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(
    methods=["post"],
    detail=False,
    url_path="create-permissions",
    permission_classes=[IsAuthenticated]
    )
    def create_permission(self, request, *args, **kwargs):
        user = request.user
        data = self.get_serializer(user).data
        instance = self.Meta.model(kwargs)
        print (instance)
        # permission_service = CustomPermisions
        # permission = permission_service.create_permission("Add vet", "abattoir")
        return Response(data)
    
    @action(
    methods=["get"],
    detail=False,
    url_path="get-user",
    permission_classes=[IsAuthenticated]
    )
    def getUser(self, request, *args, **kwargs):
        user = request.user
        data = self.get_serializer(user).data
        return CustomSuccessResponse(data)
    
    @action(
    methods=["post"],
    detail=False,
    url_path="create-group",
    permission_classes=[IsAuthenticated]
    )
    def createGroup(self, request, *args, **kwargs):
        user = request.user
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.is_admin:
            return CustomErrorResponse({'Unauthorized user':'You are not an admin.'})
        user_service = UserService()
        group = user_service.CreateGroup(request.name)
        return CustomSuccessResponse(group, status = 201)
    
class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['post'], url_path="create-group")
    def create_groups(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user_service = UserService()
            group = user_service.CreateGroup(serializer.validated_data['name'])
            data = {
                'id':group.id,
                'name':group.name
            }
        except:
            return CustomErrorResponse({'Group':'Unable to create Group'})
        return CustomSuccessResponse(data, status = 201)
   
class PermissionViewSet(viewsets.ModelViewSet):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
class ContentTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
class LogoutView(TokenBlacklistView):
    serializer_class = TokenBlacklistSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response({"message": "Logged out successfully.", "status": "success"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"message": "Token is blacklisted.", "status": "failed"},
                            status=status.HTTP_400_BAD_REQUEST)