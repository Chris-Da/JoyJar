from django.urls import path
from django.http import JsonResponse
from .views import (
    UserRegistrationView,
    UserProfileView,
    MoodTrackerView,
    router,
    JournalEntryCreateView,
    NoteCreateView,
    ChangePasswordView,
)

app_name = "users"
def test(request):
    return JsonResponse({"message": "Users app is working"})

# Combine the router's auto-generated URLs and custom paths
urlpatterns = router.urls + [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('mood/', MoodTrackerView.as_view(), name='mood-tracker'),
    path('journal-entry/', JournalEntryCreateView.as_view(), name='journal-entry-create'),
    path('note/', NoteCreateView.as_view(), name='note-create'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
