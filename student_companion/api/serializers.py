from django.conf import settings
from rest_framework import serializers
from api.models import ActivityMonitor, Flashcard, FlashcardUser
from api.models import FlashDeck
from api.models import ScUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


class FlashDeckSerializer(serializers.ModelSerializer):
    """
        Description:
            Serializer for Deck wrt FlashDeck model, will convert python object to angular understandable list
    """
    class Meta:
        model = FlashDeck
        fields = ['id', 'title']


class FlashCardSerializer(serializers.ModelSerializer):
    """
        Description:
            Serializer for Flashcards wrt FlashCard model, will convert python object to angular understandable list
    """
    class Meta:
        model = Flashcard
        fields = ['id', 'title', 'question','answer','next_scheduled_at']

class FlashCardUserSerializer(serializers.ModelSerializer):
    """
        Description:
            Serializer for FlashCard user history wrt FlashCardUser model, will convert python object to angular understandable list
    """
    class Meta:
        model = FlashcardUser
        fields = ['id', 'last_opened', 'last_time_taken','next_scheduled_at']

class ActivityMonitorSerializer(serializers.ModelSerializer):
    """
        Description:
            Serializer for ActivityMonitor model, will convert python object to angular understandable list
    """
    class Meta:
        model = ActivityMonitor
        fields = ['id', 'date', 'user_id','time_spent','cards_seen']



class UserSerializer(serializers.ModelSerializer):
    """
        Description:
            Serializer for user model that will give information of user registered
    """
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'username', 'email']




class RegisterSerializer(serializers.ModelSerializer):
    """
        Description:
            Serializer for Regisered user details 
    """
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=get_user_model().objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        """
        Description:
            Validates renter password field
        
        Input:
            attrs- first time password
        Output:
            returns password if same else raises error
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Description:
            Serializer for Flashcards wrt FlashCard model, will convert python object to angular understandable list

        Input: Gets validated data during registration
        Output: Returns object with user info
        """
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
