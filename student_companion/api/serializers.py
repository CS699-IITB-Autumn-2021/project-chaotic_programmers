from rest_framework import serializers
from api.models import TestModel
from api.models import FlashDeck

class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']

class FlashDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashDeck
        fields = ['id', 'title', 'owner_id', 'created_at', 'updated_at']