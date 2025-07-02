from django.core.management.base import BaseCommand
from chatbot_api.services import ChatbotService

class Command(BaseCommand):
    help = 'Loads initial training data for the chatbot'

    def handle(self, *args, **kwargs):
        chatbot_service = ChatbotService()
        
        # Greeting patterns
        chatbot_service.add_training_data(
            intent='greeting',
            patterns=[
                'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
                'how are you', 'how\'s it going', 'what\'s up', 'greetings'
            ],
            responses=[
                'Hello! How can I help you today?',
                'Hi there! How are you feeling?',
                'Hey! I\'m here to listen and support you. What\'s on your mind?',
                'Greetings! How can I assist you today?'
            ]
        )

        # Feeling sad patterns
        chatbot_service.add_training_data(
            intent='feeling_sad',
            patterns=[
                'i am sad', 'i feel sad', 'i\'m feeling down', 'i\'m depressed',
                'i feel low', 'i\'m not happy', 'i feel blue', 'i\'m feeling miserable',
                'i feel hopeless', 'i\'m feeling down today'
            ],
            responses=[
                'I\'m sorry to hear that you\'re feeling sad. Would you like to talk about what\'s bothering you?',
                'It\'s okay to feel sad sometimes. I\'m here to listen if you want to share what\'s on your mind.',
                'I hear that you\'re feeling down. Remember that it\'s okay to feel this way, and I\'m here to support you.',
                'I\'m here for you. Would you like to talk about what\'s making you feel sad?'
            ]
        )

        # Feeling anxious patterns
        chatbot_service.add_training_data(
            intent='feeling_anxious',
            patterns=[
                'i am anxious', 'i feel anxious', 'i\'m worried', 'i feel nervous',
                'i\'m feeling stressed', 'i have anxiety', 'i\'m feeling overwhelmed',
                'i can\'t stop worrying', 'i feel tense', 'my mind is racing'
            ],
            responses=[
                'I understand that anxiety can be really challenging. Would you like to talk about what\'s causing your anxiety?',
                'It\'s common to feel anxious sometimes. I\'m here to listen if you want to share what\'s worrying you.',
                'I hear that you\'re feeling anxious. Remember to take deep breaths. Would you like to talk about what\'s on your mind?',
                'I\'m here to support you through this anxiety. What\'s making you feel this way?'
            ]
        )

        # Gratitude patterns
        chatbot_service.add_training_data(
            intent='gratitude',
            patterns=[
                'thank you', 'thanks', 'i appreciate it', 'that\'s helpful',
                'you\'re helpful', 'you\'re great', 'that\'s kind of you',
                'i\'m grateful', 'thanks for listening', 'you\'re a good listener'
            ],
            responses=[
                'You\'re welcome! I\'m glad I could help.',
                'It\'s my pleasure to be here for you.',
                'Thank you for sharing with me. I\'m here whenever you need to talk.',
                'I\'m happy to help! Is there anything else you\'d like to discuss?'
            ]
        )

        # Goodbye patterns
        chatbot_service.add_training_data(
            intent='goodbye',
            patterns=[
                'bye', 'goodbye', 'see you later', 'talk to you later',
                'i have to go', 'i\'m leaving', 'take care', 'farewell'
            ],
            responses=[
                'Take care! I\'m here if you need to talk again.',
                'Goodbye! Remember that I\'m always here to listen.',
                'See you later! Take care of yourself.',
                'Farewell! Don\'t hesitate to reach out if you need support.'
            ]
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial training data')) 