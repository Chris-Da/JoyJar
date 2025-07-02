from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, ChatSession, Message, Resource, ChatInteraction, TrainingData

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'date_of_birth', 'emergency_contact',
                 'preferred_language', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'content', 'is_user', 'timestamp', 'sentiment_score',
                 'emotion_detected', 'requires_attention', 'flagged_keywords')
        read_only_fields = ('timestamp', 'sentiment_score', 'emotion_detected',
                          'requires_attention', 'flagged_keywords')

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ChatSession
        fields = ('id', 'username', 'created_at', 'updated_at', 'is_active',
                 'initial_mood', 'session_notes', 'requires_follow_up',
                 'follow_up_date', 'messages')
        read_only_fields = ('created_at', 'updated_at')

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'title', 'description', 'resource_type', 'url',
                 'content', 'created_at', 'updated_at', 'is_active', 'tags')
        read_only_fields = ('created_at', 'updated_at')

class ChatInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInteraction
        fields = ['id', 'message', 'response', 'created_at', 'feedback']
        read_only_fields = ['response', 'created_at']

class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = ['id', 'intent', 'patterns', 'responses', 'context'] 