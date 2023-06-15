from django.urls import path
from .views import GeneralClassView
from rest_framework import routers
from apps.accounts import views

urlpatterns = [
    path('user', GeneralClassView.as_view())
]

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"accounts", views.UserViewSet)

urlpatterns = []

urlpatterns += router.urls