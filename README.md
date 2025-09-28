# Simple Q&A Chatbot with Django and ChatterBot

A terminal-based conversational AI chatbot built using Django and the ChatterBot library. This project provides an interactive command-line interface for natural language conversations.

## Features

- **Real ChatterBot Integration**: Uses the official ChatterBot library for natural language processing
- **Django Framework**: Built on Django for robust project structure and management commands
- **Persistent Learning**: SQLite database storage for conversation history and learning
- **Pre-trained Conversations**: Comes with conversational training data for immediate use
- **Terminal Interface**: Clean command-line chat interface with graceful input handling
- **Python 3.11 Compatible**: Resolved compatibility issues with modern Python versions

### Prerequisites

- Python 3.11 (recommended for compatibility)
- pip (Python package installer)
- Git (for cloning)

### Installation

1. **Clone or download the project** to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd "Simple Q&A Chatbot with Python"
   ```

3. **Run the chatbot using the provided batch file**:
   ```bash
   start_chatbot.bat
   ```

   Or manually with:
   ```bash
   .\venv_chatbot\Scripts\python.exe manage.py chat
   ```

## Example Conversation

```
Chat started! Type 'exit', 'quit', or 'bye' to end the conversation.
Try saying: 'Good morning! How are you doing?'
==================================================
You: Good morning! How are you doing?
ChatBot: I am doing very well, thank you for asking.

You: Hello
ChatBot: Hi there! How can I help you today?

You: How are you?
ChatBot: I'm doing great, thanks for asking!

You: What's your name?
ChatBot: My name is ChatBot. What's yours?

You: Tell me a joke
ChatBot: Why don't scientists trust atoms? Because they make up everything!

You: exit
ChatBot: Goodbye! It was nice chatting with you!
```

## Project Structure

```
Simple Q&A Chatbot with Python/
├── manage.py                    # Django management script
├── start_chatbot.bat           # Easy launcher for Windows
├── test_chatterbot.py          # Test script to verify functionality
├── README.md                   # This file
├── .gitignore                  # Git ignore patterns
├── requirements.txt            # Python dependencies (if generated)
├── chatbot_project/            # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Django configuration
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI configuration
├── bot/                        # Django app for chatbot
│   ├── __init__.py
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models (empty)
│   ├── views.py               # Web views (empty)
│   └── management/
│       └── commands/
│           ├── __init__.py
│           └── chat.py        # Main chat command
└── venv_chatbot/              # Virtual environment (not in git)
    └── ...                    # Python packages and dependencies
```

## Technical Details

### Dependencies

- **Django 4.2.24**: Web framework for project structure and management commands
- **ChatterBot 1.2.7**: Natural language processing and conversation engine
- **spaCy 3.8.7**: Natural language processing library used by ChatterBot
- **SQLAlchemy 2.0.43**: Database ORM for conversation storage
- **Additional dependencies**: See `pip list` in virtual environment for complete list

### Database

- **Storage**: SQLite database (`chatbot_db.sqlite3`)
- **Purpose**: Stores conversation history and learned responses
- **Location**: Project root directory

### Virtual Environment

The project uses a Python 3.11 virtual environment (`venv_chatbot`) to ensure compatibility and dependency isolation.

## Development Setup

If you need to set up the development environment from scratch:

1. **Create virtual environment**:
   ```bash
   python -m venv venv_chatbot
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   .\venv_chatbot\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv_chatbot/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install Django==4.2.24 chatterbot==1.2.7 pyyaml
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the chatbot**:
   ```bash
   python manage.py chat
   ```

## Training Data

The chatbot comes pre-trained with conversational pairs including:

- Greetings and responses
- Basic questions and answers  
- Polite conversation patterns
- Jokes and fun interactions

You can modify the training data in `bot/management/commands/chat.py` in the `conversations` list.

## Commands

- **Start Chat**: `python manage.py chat`
- **Database Migration**: `python manage.py migrate`
- **Test Installation**: `python test_chatterbot.py`

### Exit Commands

During chat, you can exit using:
- `exit`
- `quit` 
- `bye`
- `goodbye`
- `Ctrl+C`

## Troubleshooting

### Common Issues

1. **"ChatterBot import error"**: 
   - Ensure you're using the virtual environment Python
   - Run: `.\venv_chatbot\Scripts\python.exe manage.py chat`

2. **"Module not found"**:
   - Activate virtual environment: `.\venv_chatbot\Scripts\Activate.ps1`
   - Verify installation: `pip list`

3. **"Database errors"**:
   - Run migrations: `python manage.py migrate`
   - Delete `chatbot_db.sqlite3` to reset

4. **Python version compatibility**:
   - Use Python 3.11 for best compatibility
   - Avoid Python 3.12+ due to typing module changes

### Performance Notes

- First run may be slower due to spaCy model loading
- Subsequent runs are faster with cached models
- Training occurs on each startup (normal behavior)

This is an educational project. Feel free to:

1. Add more training data for better responses
2. Implement additional logic adapters
3. Create a web interface using Django views
4. Add more sophisticated NLP features

##  References

- [ChatterBot Documentation](https://chatterbot.readthedocs.io/)
- [Django Documentation](https://docs.djangoproject.com/)
- [spaCy Documentation](https://spacy.io/usage)


**Happy Chatting!**