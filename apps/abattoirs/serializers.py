from rest_framework import serializers
from apps.abattoirs.models import Abattoir

class AbattoirSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Abattoir
        fields = '__all__'