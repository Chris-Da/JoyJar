import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import TrainingData, ChatInteraction
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class ChatbotService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self._training_data = None
        self._patterns = None
        self._responses = None
        self._intents = None

    @property
    def training_data(self):
        if self._training_data is None:
            self.load_training_data()
        return self._training_data

    @property
    def patterns(self):
        if self._patterns is None:
            self.load_training_data()
        return self._patterns

    @property
    def responses(self):
        if self._responses is None:
            self.load_training_data()
        return self._responses

    @property
    def intents(self):
        if self._intents is None:
            self.load_training_data()
        return self._intents

    def load_training_data(self):
        """Load and prepare training data from the database"""
        try:
            self._training_data = list(TrainingData.objects.all())
            self._patterns = []
            self._responses = []
            self._intents = []

            for data in self._training_data:
                patterns = data.get_patterns()
                responses = data.get_responses()
                self._patterns.extend(patterns)
                self._responses.extend(responses)
                self._intents.extend([data.intent] * len(patterns))

            print(f"DEBUG: Loaded patterns: {self._patterns}")
            print(f"DEBUG: Loaded intents: {self._intents}")

            if self._patterns:
                # Fit the vectorizer with all patterns
                self.vectorizer.fit(self._patterns)
        except Exception as e:
            print(f"Error loading training data: {e}")
            self._training_data = []
            self._patterns = []
            self._responses = []
            self._intents = []

    def preprocess_text(self, text):
        """Preprocess the input text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)

    def get_response(self, user_message, user=None):
        """Get the most appropriate response for the user message"""
        if not self.patterns:
            return "I'm still learning. Please try again later."

        # Preprocess the user message
        processed_message = self.preprocess_text(user_message)
        
        # Transform the processed message
        message_vector = self.vectorizer.transform([processed_message])
        patterns_vector = self.vectorizer.transform(self.patterns)
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(message_vector, patterns_vector)[0]
        
        # Get the index of the most similar pattern
        best_match_idx = np.argmax(similarity_scores)
        best_match_score = similarity_scores[best_match_idx]
        
        # If the best match score is too low, return a default response
        if best_match_score < 0.3:
            response = "I'm not sure I understand. Could you rephrase that?"
        else:
            # Get the corresponding response
            intent = self.intents[best_match_idx]
            matching_data = next((data for data in self.training_data if data.intent == intent), None)
            
            if matching_data and matching_data.responses:
                try:
                    # Load and parse the responses
                    raw_responses = matching_data.responses
                    print(f"Raw responses: {raw_responses}")  # Debugging line to print raw responses
                    
                    if isinstance(raw_responses, str):
                        responses_list = json.loads(raw_responses)
                        if isinstance(responses_list, str):
                            responses_list = [responses_list]
                    elif isinstance(raw_responses, list):
                        responses_list = raw_responses
                    else:
                        responses_list = [str(raw_responses)]

                    # Ensure it's a list of strings and validate the list
                    responses_list = [str(r) for r in responses_list if isinstance(r, (str, int, float))]

                    # Debugging the list after filtering for valid values
                    print(f"Filtered responses list: {responses_list}")

                    # Ensure responses_list is a proper 1-dimensional array
                    if len(responses_list) == 0:
                        response = "I'm not sure how to respond to that."
                    else:
                        # Ensure it's a 1-dimensional list (flatten if necessary)
                        responses_list = np.array(responses_list).flatten()

                        # Print the flattened responses list
                        print(f"Flattened responses list (size: {responses_list.size}): {responses_list}")

                        # If it's still not a valid 1-dimensional list, return a fallback message
                        if responses_list.size == 0:
                            response = "I'm not sure how to respond to that."
                        else:
                            # Choose a random response from the valid list
                            response = np.random.choice(responses_list)
                except Exception as e:
                    print(f"Error parsing responses: {e}")
                    response = "I'm not sure how to respond to that."
            else:
                response = "I'm not sure how to respond to that."

        # Save the interaction
        try:
            ChatInteraction.objects.create(
                user=user,
                message=user_message,
                response=response
            )
        except Exception as e:
            print(f"Error saving chat interaction: {e}")

        return response



    def add_training_data(self, intent, patterns, responses, context=''):
        """Add new training data to the database"""
        training_data = TrainingData.objects.create(
            intent=intent,
            context=context
        )
        training_data.set_patterns(patterns)
        training_data.set_responses(responses)
        training_data.save()
        self.load_training_data()  # Reload training data
        return training_data

    def get_feedback(self, interaction_id, feedback):
        """Update the feedback for a chat interaction"""
        try:
            interaction = ChatInteraction.objects.get(id=interaction_id)
            interaction.feedback = feedback
            interaction.save()
            return True
        except ChatInteraction.DoesNotExist:
            return False
