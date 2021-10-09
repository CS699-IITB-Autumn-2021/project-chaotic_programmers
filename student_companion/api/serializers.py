from rest_framework import serializers
from api.models import TestModel

class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']