from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, JournalEntrySerializer, NoteSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from .models import JournalEntry
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.routers import DefaultRouter
from django.urls import path

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': serializer.data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MoodTrackerView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        mood = request.data.get('mood')
        if not mood:
            return Response({'error': 'Mood is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Here you would typically save the mood to a database
        # For now, we'll just return a success response
        return Response({
            'message': 'Mood recorded successfully',
            'mood': mood,
            'timestamp': timezone.now()
        }, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'detail': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Find user by email
        try:
            user = User.objects.get(email=email)
            # Authenticate with username and password
            user = authenticate(username=user.username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                })
            else:
                return Response({
                    'detail': 'Invalid email or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({
                'detail': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

class JournalEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JournalEntrySerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
        return super().get_permissions()

class JournalEntryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JournalEntrySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password or len(new_password) < 6:
            return Response({'error': 'New password must be at least 6 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

# Update the router registration
router = DefaultRouter()
router.register(r'journal', JournalEntryViewSet, basename='journal-entries')

# Update the URL patterns in urls.py
def get_urlpatterns():
    return [
        path('register/', UserRegistrationView.as_view(), name='user-register'),
        path('profile/', UserProfileView.as_view(), name='user-profile'),
        path('mood/', MoodTrackerView.as_view(), name='mood-tracker'),
    ]

# Export the router for use in urls.py
__all__ = ['router', 'get_urlpatterns']
