import warnings
import sys
from django.core.management.base import BaseCommand, CommandError

# Suppress deprecation warnings from ChatterBot and typing module
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore")

def _safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return 'exit'
    except KeyboardInterrupt:
        print("\n^C")
        return 'exit'


class Command(BaseCommand):
    help = 'Start a terminal chat session with ChatterBot.'

    def add_arguments(self, parser):
        parser.add_argument('--name', default='ChatBot', help='Bot name (storage identification)')
        parser.add_argument('--read-only', action='store_true', help='Disable learning from conversation')

    def handle(self, *args, **options):
        # Import ChatterBot here to handle any import errors gracefully
        try:
            from chatterbot import ChatBot
            from chatterbot.trainers import ListTrainer
        except ImportError as e:
            raise CommandError(
                f'ChatterBot is not installed or has compatibility issues.\n'
                f'Try: pip install chatterbot\n'
                f'Original error: {e}'
            )
        except Exception as e:
            raise CommandError(
                f'Failed to import ChatterBot. This may be a compatibility issue.\n'
                f'Original error: {e}'
            )

        bot_name = options['name']
        read_only = options['read_only']

        # Configure ChatterBot with improved settings for better context awareness
        try:
            chatbot = ChatBot(
                bot_name,
                read_only=read_only,
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri='sqlite:///chatbot_db.sqlite3',
                logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': "I understand! What would you like to chat about?",
                        'maximum_similarity_threshold': 0.70,  # Even lower for better fuzzy matching
                        'response_selection_method': 'chatterbot.response_selection.get_most_frequent_response'
                    }
                ],
            )
        except Exception as e:
            raise CommandError(f'Failed to initialize ChatBot: {e}')

        # Train the bot with conversational examples
        try:
            trainer = ListTrainer(chatbot)
            
            # Enhanced conversational training data with better context awareness
            conversations = [
                # Main example from user request
                "Good morning! How are you doing?",
                "I am doing very well, thank you for asking.",
                
                # Greeting variations
                "Hi! How are you?",
                "Hello! I'm doing great, thanks for asking. How are you today?",
                "Hey there! How are you?", 
                "Hi! I'm doing well, thank you. What brings you here today?",
                "Hello",
                "Hi there! How can I help you today?",
                "Hey",
                "Hey! Great to chat with you. How's everything going?",
                "Good morning",
                "Good morning! Hope you're having a wonderful day!",
                "Good afternoon", 
                "Good afternoon! How has your day been so far?",
                "Good evening",
                "Good evening! How was your day?",
                
                # Positive statements and appropriate responses
                "It is a great day!",
                "That's wonderful to hear! What's making your day so great?",
                "I'm having a wonderful time!",
                "That's fantastic! I'm glad you're enjoying yourself.",
                "Today has been amazing!",
                "How exciting! I'd love to hear what made it so amazing.",
                "I'm feeling really good today!",
                "That's great news! A positive attitude can make such a difference.",
                "Things are going really well!",
                "I'm so happy to hear that! It sounds like everything is falling into place.",
                
                # Offers of help and appropriate responses  
                "How can I help you?",
                "That's very kind of you to offer! I'm here to chat and answer questions. Is there anything you'd like to talk about?",
                "Can I assist you with something?",
                "Thank you for asking! I enjoy our conversation. What would you like to discuss?",
                "Do you need any help?",
                "I appreciate your thoughtfulness! I'm doing fine, but I'd love to help you with anything you need.",
                "Is there anything I can do for you?",
                "You're very considerate! I'm here if you have any questions or just want to chat.",
                
                # Personal questions
                "What's your name?",
                "I'm ChatBot, your friendly AI assistant. What should I call you?",
                "Who are you?",
                "I'm an AI chatbot created to have conversations and help answer questions. Nice to meet you!",
                "Tell me about yourself",
                "I'm an AI designed to chat and learn from conversations. I enjoy talking about various topics. What about you?",
                
                # Interests and hobbies
                "What do you like to do?",
                "I enjoy having conversations and learning new things from the people I chat with. What are your hobbies?",
                "What are your interests?",
                "I find human conversations fascinating! I'm curious about everything from science to art. What interests you?",
                "I like reading",
                "Reading is wonderful! What kind of books do you enjoy?",
                "I enjoy science fiction",
                "Science fiction is fascinating! Have you read any good books lately?",
                "I love music",
                "Music is amazing! What genres or artists do you like?",
                "I'm into sports",
                "Sports are exciting! Which sports do you follow or play?",
                
                # Compliments and reactions
                "That's interesting",
                "Thank you! What about you? What are your interests?",
                "That's cool",
                "I'm glad you think so! What do you find interesting?",
                "Nice!",
                "Thanks! I try to be helpful and engaging. What would you like to chat about?",
                "Awesome!",
                "Great to hear you're excited! What's got you feeling so positive?",
                
                # Information requests
                "What's the weather like?",
                "I don't have access to current weather data, but I hope it's nice where you are! How's the weather on your end?",
                "What time is it?",
                "I don't have access to the current time, but you can check your device's clock. Are you planning something special?",
                
                # Jokes and humor - multiple jokes to avoid repetition
                "Tell me a joke",
                "Why don't scientists trust atoms? Because they make up everything!",
                "Tell me another joke",
                "What do you call a fake noodle? An impasta!",
                "Do you know any jokes?",
                "Here's one: Why did the scarecrow win an award? Because he was outstanding in his field!",
                "Can you tell me a funny joke?",
                "Sure! What do you call a sleeping bull? A bulldozer!",
                "I want to hear a joke",
                "Why don't eggs tell jokes? They'd crack each other up!",
                
                # Responses to joke reactions
                "That's funny",
                "I'm glad you enjoyed it! Do you know any good jokes?",
                "That's hilarious",
                "Great! I love making people laugh. Want to hear another one?",
                "Haha",
                "I'm happy I could make you laugh! Humor is so important.",
                "LOL",
                "Awesome! Laughter is the best medicine, they say!",
                
                # Responses about not knowing jokes
                "Not really",
                "No worries at all! Not everyone is into jokes. What do you enjoy for fun?",
                "I don't know any jokes",
                "That's perfectly fine! Would you like me to tell you another one, or shall we talk about something else?",
                "I'm not good at jokes",
                "Don't worry about it! Everyone has different talents. What are you good at?",
                "No, I don't know jokes",
                "No problem! I can tell you more if you'd like, or we can chat about other topics. What interests you?",
                
                # About AI/technology
                "How old are you?",
                "As an AI, I don't age like humans do. I was created recently and I'm always learning! How long have you been interested in AI?",
                "Where are you from?",
                "I exist in the digital realm, created by developers using Python and ChatterBot. Where are you from?",
                "What can you do?",
                "I can have conversations, answer questions, and learn from our interactions. I enjoy discussing various topics! What would you like to talk about?",
                "Are you real?",
                "I'm a real AI program, though I'm not human. I exist as software and love chatting with real people like you!",
                
                # Gratitude and politeness
                "Thanks",
                "You're very welcome! Is there anything else I can help you with?",
                "Thank you",
                "You're welcome! I'm glad I could help. What else would you like to discuss?",
                "I appreciate it",
                "I'm happy to help! That's what I'm here for. Anything else on your mind?",
                
                # Farewells
                "Nice to meet you",
                "Nice to meet you too! I'm enjoying our conversation already.",
                "Have a good day",
                "Thank you, you too! Feel free to come back and chat anytime.",
                "See you later",
                "See you later! Thanks for the great conversation!",
                "Goodbye",
                "Goodbye! It was really nice talking with you today.",
                
                # Negative or uncertain responses
                "I don't know",
                "That's okay! Is there something specific you'd like to know about, or would you like to explore a different topic?",
                "I'm not sure",
                "No problem! Sometimes we're all uncertain about things. What would you like to talk about?",
                "Maybe",
                "Fair enough! Sometimes 'maybe' is the most honest answer. What are you thinking about?",
                "I guess",
                "I understand the uncertainty! What's on your mind that you're unsure about?",
                "Sort of",
                "I get it - sometimes things are complicated! Want to talk more about it?",
                
                # Specific requests for more jokes after saying they don't know any
                "I do not know any jokes tell me another joke",
                "No problem! Here's another one: What do you call a sleeping bull? A bulldozer!",
                "I don't know jokes tell me more",
                "Sure! How about this: Why don't eggs tell jokes? They'd crack each other up!",
                "I am not good at jokes give me another",
                "Of course! Here's one: What do you call a fake noodle? An impasta!",
                "Tell me more jokes I don't know any",
                "Happy to! Why did the scarecrow win an award? Because he was outstanding in his field!",
                
                # Requests for more content
                "Tell me more",
                "I'd be happy to! What specifically would you like to know more about?",
                "Can you elaborate?",
                "Of course! What aspect would you like me to go deeper into?",
                "Give me details",
                "Sure thing! What kind of details are you looking for?",
                
                # Conversation flow and general responses
                "How's your day going?",
                "Every day is interesting for me since I get to meet new people! How's your day treating you?",
                "What's new?",
                "Every conversation brings something new for me! What's new and exciting in your world?",
                "How are things?",
                "Things are good on my end! I'm always ready for a good chat. How are things with you?",
                "What should we talk about?",
                "Great question! I enjoy discussing all sorts of topics. What interests you most?",
                "I'm bored",
                "Let's fix that! What usually gets you excited or interested? We could talk about hobbies, current events, or I could tell you some jokes!",
            ]
            
            # Train in pairs
            for i in range(0, len(conversations), 2):
                if i + 1 < len(conversations):
                    trainer.train([conversations[i], conversations[i + 1]])
            
            self.stdout.write(self.style.SUCCESS(f'{bot_name} has been trained and is ready to chat!'))
        
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Training failed: {e}'))
            self.stdout.write(self.style.NOTICE('Continuing without additional training...'))

        self.stdout.write(self.style.SUCCESS(f"Chat started! Type 'exit', 'quit', or 'bye' to end the conversation."))
        self.stdout.write(self.style.SUCCESS(f"Try saying: 'Good morning! How are you doing?'"))
        self.stdout.write(self.style.WARNING("=" * 50))

        # Terminal chat loop
        while True:
            try:
                text = _safe_input('You: ').strip()
            except Exception as e:
                self.stderr.write(f'Input error: {e}')
                break

            if not text:
                continue
                
            if text.lower() in {'exit', 'quit', 'bye', 'goodbye'}:
                self.stdout.write('ChatBot: Goodbye! It was nice chatting with you!')
                break

            try:
                response = chatbot.get_response(text)
                self.stdout.write(f'ChatBot: {response}')
            except KeyboardInterrupt:
                self.stdout.write('\nChatBot: Goodbye!')
                break
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error generating response: {e}'))

        # Clean shutdown
        try:
            if hasattr(chatbot.storage, 'session') and chatbot.storage.session:
                chatbot.storage.session.close()
        except Exception:
            pass