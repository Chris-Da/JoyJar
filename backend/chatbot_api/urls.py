from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.views.generic import RedirectView
from .views import ChatbotView, FeedbackView, TrainingDataView, GeminiChatView, OpenAIChatView, ChatterBotChatView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'sessions', views.ChatSessionViewSet, basename='session')
router.register(r'resources', views.ResourceViewSet, basename='resource')

# Nested router for messages within sessions
from rest_framework_nested import routers
session_router = routers.NestedDefaultRouter(router, r'sessions', lookup='session')
session_router.register(r'messages', views.MessageViewSet, basename='session-messages')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(session_router.urls)),
    path("auth/", include('rest_framework.urls')),
    path('chat/', ChatbotView.as_view(), name='chatbot-chat'),
    path('feedback/', FeedbackView.as_view(), name='chatbot-feedback'),
    path('training/', TrainingDataView.as_view(), name='chatbot-training'),
    path('training/<int:intent_id>/', TrainingDataView.as_view(), name='chatbot-training-delete'),
    path('chatbot/', GeminiChatView.as_view(), name='gemini-chat'),
    path('openai-chat/', OpenAIChatView.as_view(), name='openai-chat'),
    path('chatterbot-chat/', ChatterBotChatView.as_view(), name='chatterbot-chat'),
] 