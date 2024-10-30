
from rest_framework import serializers
from .models import ProductMetrics

class ProductMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMetrics
        fields = ['date', 'signups', 'transcribed_cases', 'active_users', 'average_processing_time']
