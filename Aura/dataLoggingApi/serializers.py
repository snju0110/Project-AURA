from rest_framework import serializers
from .models import *


class demDataLoggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = demDatatable
        fields = '__all__'


class demDailyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = demDailyData
        fields = '__all__'