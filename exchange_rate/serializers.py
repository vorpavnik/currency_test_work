import pytz
from rest_framework import serializers
from .models import ExchangeRate

class ExchangeRateSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = ExchangeRate
        fields = ['rate', 'timestamp']

    def get_timestamp(self, obj):
        moscow_time = obj.timestamp.astimezone(pytz.timezone("Europe/Moscow"))
        return moscow_time.strftime("%d-%m-%Y %H-%M")