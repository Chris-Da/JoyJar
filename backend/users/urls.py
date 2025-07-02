from django.urls import path
from django.http import JsonResponse
from .views import (
    UserRegistrationView,
    UserProfileView,
    MoodTrackerView,
    router,
)

app_name = "users"
def test(request):
    return JsonResponse({"message": "Users app is working"})

# Combine the router's auto-generated URLs and custom paths
urlpatterns = router.urls + [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('mood/', MoodTrackerView.as_view(), name='mood-tracker'),
]
