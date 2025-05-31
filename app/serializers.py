from rest_framework import serializers
from .models import Presente

class PresenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presente
        fields = '__all__'