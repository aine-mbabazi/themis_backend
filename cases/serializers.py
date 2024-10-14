# serializers.py

from api import serializers
from .models import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'is_transcribed']
