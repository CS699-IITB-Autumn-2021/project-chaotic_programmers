from rest_framework import serializers
from api.models import Flashcard, TestModel
from api.models import FlashDeck
from api.models import User

class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']

class FlashDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashDeck
        fields = ['id', 'title', 'owner_id']


class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'title', 'question','answer','owner_id','flash_deck_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email_id', 'username']