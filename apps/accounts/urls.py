from django.urls import path
from .views import GeneralClassView, LogoutView
from rest_framework import routers
from apps.accounts import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('user', GeneralClassView.as_view()),
    path('logout/blacklist/', LogoutView.as_view(),
         name='blacklist'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"accounts", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)

urlpatterns += router.urls