from rest_framework import serializers
from .models import Service, Booking, Professional

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class DisponibilidadeSerializer(serializers.Serializer):
    horarios_disponiveis = serializers.ListField(
        child=serializers.CharField()
    )
    ocupados = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField())
    )

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['id', 'name', 'bio', 'photo']