from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class JournalEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('calm', 'Calm'),
        ('neutral', 'Neutral'),
        ('anxious', 'Anxious'),
        ('sad', 'Sad'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    content = models.TextField()
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'

    def __str__(self):
        return f"Journal Entry by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note: {self.title} by {self.user.username}"
