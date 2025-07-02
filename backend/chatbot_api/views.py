from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile, ChatSession, Message, Resource, ChatInteraction, TrainingData
from .serializers import (
    UserProfileSerializer,
    ChatSessionSerializer,
    MessageSerializer,
    ResourceSerializer,
    UserSerializer,
    ChatInteractionSerializer,
    TrainingDataSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db import models
import json
from rest_framework.views import APIView
from .services import ChatbotService

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        session = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response(
                {'error': 'Message content is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user message
        user_message = Message.objects.create(
            session=session,
            content=content,
            is_user=True
        )

        # TODO: Implement your chatbot logic here
        # For now, we'll just echo back a simple response
        bot_response = Message.objects.create(
            session=session,
            content="I understand you're feeling this way. Would you like to talk more about it?",
            is_user=False
        )

        return Response({
            'user_message': MessageSerializer(user_message).data,
            'bot_response': MessageSerializer(bot_response).data
        })

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        session_id = self.kwargs.get('session_pk')
        return Message.objects.filter(
            session_id=session_id,
            session__user=self.request.user
        )

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.filter(is_active=True)
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        resource_type = request.query_params.get('type')
        if resource_type:
            resources = self.queryset.filter(resource_type=resource_type)
            serializer = self.get_serializer(resources, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Resource type is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            # Search in title and description
            resources = self.queryset.filter(
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query)
            )
            # Also search in tags
            resources = [r for r in resources if query.lower() in [t.lower() for t in r.get_tags()]]
            serializer = self.get_serializer(resources, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Search query is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

chatbot_service = ChatbotService()

class ChatbotView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow both authenticated and anonymous users

    def post(self, request):
        """Handle incoming chat messages"""
        message = request.data.get('message', '').strip()
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get user if authenticated
        user = request.user if request.user.is_authenticated else None

        # Get response from chatbot
        response = chatbot_service.get_response(message, user)

        # Get the latest interaction for feedback
        interaction = ChatInteraction.objects.filter(
            message=message,
            response=response
        ).order_by('-created_at').first()

        return Response({
            'response': response,
            'interaction_id': interaction.id if interaction else None
        })

class FeedbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle feedback for chat interactions"""
        interaction_id = request.data.get('interaction_id')
        feedback = request.data.get('feedback')

        if interaction_id is None or feedback is None:
            return Response(
                {'error': 'Both interaction_id and feedback are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        success = chatbot_service.get_feedback(interaction_id, feedback)
        if success:
            return Response({'message': 'Feedback recorded successfully'})
        return Response(
            {'error': 'Interaction not found'},
            status=status.HTTP_404_NOT_FOUND
        )

class TrainingDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can manage training data

    def get(self, request):
        """Get all training data"""
        training_data = TrainingData.objects.all()
        serializer = TrainingDataSerializer(training_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Add new training data"""
        serializer = TrainingDataSerializer(data=request.data)
        if serializer.is_valid():
            training_data = chatbot_service.add_training_data(
                intent=serializer.validated_data['intent'],
                patterns=serializer.validated_data['patterns'],
                responses=serializer.validated_data['responses'],
                context=serializer.validated_data.get('context', '')
            )
            return Response(
                TrainingDataSerializer(training_data).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, intent_id):
        """Delete training data"""
        training_data = get_object_or_404(TrainingData, id=intent_id)
        training_data.delete()
        chatbot_service.load_training_data()  # Reload training data
        return Response(status=status.HTTP_204_NO_CONTENT)
