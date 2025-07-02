from django.core.management.base import BaseCommand
from chatbot_api.services import ChatbotService
import json

class Command(BaseCommand):
    help = 'Add new training data to the chatbot'

    def add_arguments(self, parser):
        parser.add_argument('intent', type=str, help='Intent name')
        parser.add_argument('patterns', type=str, help='JSON list of patterns')
        parser.add_argument('responses', type=str, help='JSON list of responses')
        parser.add_argument('--context', type=str, default='', help='Optional context')

    def handle(self, *args, **kwargs):
        intent = kwargs['intent']
        patterns = json.loads(kwargs['patterns'])
        responses = json.loads(kwargs['responses'])
        context = kwargs['context']

        chatbot_service = ChatbotService()
        training_data = chatbot_service.add_training_data(intent, patterns, responses, context)

        self.stdout.write(self.style.SUCCESS(f'Successfully added training data for intent: {intent}'))
