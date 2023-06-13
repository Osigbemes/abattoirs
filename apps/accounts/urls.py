from django.urls import path
from .views import GeneralClassView

urlpatterns = [
    path('', GeneralClassView.as_view())
]