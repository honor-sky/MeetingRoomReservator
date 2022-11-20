from rest_framework.serializers import ModelSerializer
from .models import Roomreservation, Meetingroom

class TestDataSerializer(ModelSerializer):
    class Meta:
        model = Roomreservation
        fields = '__all__'

class TestDataSerializer2(ModelSerializer):
    class Meta:
        model = Meetingroom
        fields = '__all__'

class SaveReservationSerializer(ModelSerializer):
    class Meta:
        model = Roomreservation
        fields = '__all__'


