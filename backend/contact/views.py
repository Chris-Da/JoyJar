from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSubmissionSerializer
from .models import ContactSubmission

class ContactSubmissionView(APIView):
    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            # Save the submission
            submission = serializer.save()
            
            # Send email notification to admin
            try:
                subject = f"New Contact Form Submission from {submission.name}"
                message = f"""
                New contact form submission received:
                
                From: {submission.name}
                Email: {submission.email}
                Phone: {submission.phone or 'Not provided'}
                
                Message:
                {submission.message}
                
                Submitted at: {submission.submitted_at}
                """
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )

                # Send confirmation email to user
                user_subject = "Thank you for contacting JoyJar"
                user_message = f"""
                Dear {submission.name},

                Thank you for reaching out to JoyJar. We have received your message and will get back to you as soon as possible.

                Your message:
                {submission.message}

                Best regards,
                The JoyJar Team
                """
                
                send_mail(
                    subject=user_subject,
                    message=user_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[submission.email],
                    fail_silently=False,
                )

            except Exception as e:
                # Log the error but don't fail the request
                print(f"Error sending email: {str(e)}")
            
            return Response({
                'message': 'Thank you for your message. We will get back to you soon!'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 