from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(max_length=50, default='English')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ChatSession(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('anxious', 'Anxious'),
        ('stressed', 'Stressed'),
        ('neutral', 'Neutral'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    initial_mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')
    session_notes = models.TextField(blank=True)
    requires_follow_up = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat Session {self.id} - {self.user.username} ({self.initial_mood})"

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)
    sentiment_score = models.FloatField(null=True, blank=True)
    emotion_detected = models.CharField(max_length=50, blank=True)
    requires_attention = models.BooleanField(default=False)
    flagged_keywords = models.TextField(default='[]')  # Store as JSON string

    def get_flagged_keywords(self):
        try:
            return json.loads(self.flagged_keywords)
        except:
            return []

    def set_flagged_keywords(self, keywords):
        self.flagged_keywords = json.dumps(keywords)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{'User' if self.is_user else 'Bot'} message in session {self.session.id}"

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('exercise', 'Exercise'),
        ('hotline', 'Hotline'),
        ('tool', 'Tool'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    tags = models.TextField(default='[]')  # Store as JSON string

    def get_tags(self):
        try:
            return json.loads(self.tags)
        except:
            return []

    def set_tags(self, tags):
        self.tags = json.dumps(tags)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.resource_type})"

class ChatInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.BooleanField(null=True, blank=True)  # For user feedback on responses

    class Meta:
        ordering = ['-created_at']

class TrainingData(models.Model):
    intent = models.CharField(max_length=100)  # The category of the question/response
    patterns = models.TextField()  # Store JSON as text
    responses = models.TextField()  # Store JSON as text
    context = models.CharField(max_length=100, blank=True)  # Optional context for follow-up questions

    def get_patterns(self):
        try:
            return json.loads(self.patterns)
        except:
            return []

    def set_patterns(self, patterns):
        self.patterns = json.dumps(patterns)

    def get_responses(self):
        try:
            return json.loads(self.responses)
        except:
            return []

    def set_responses(self, responses):
        self.responses = json.dumps(responses)

    class Meta:
        ordering = ['intent']

    def __str__(self):
        return f"{self.intent} - {len(self.get_patterns())} patterns"
