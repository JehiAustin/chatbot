import os
import random

import openai

# Normal / greeting queries: always use these (no API call) to save quota and avoid errors
NORMAL_QUERIES = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! What would you like to know?",
    "hey": "Hey! How can I assist you?",
    "what is your name": "I'm an AI assistant. You can call me whatever you like!",
    "what's your name": "I'm an AI assistant. You can call me whatever you like!",
    "who are you": "I'm a helpful AI assistant. Ask me anything!",
    "how are you": "I'm doing well, thanks for asking! How can I help you?",
    "how are you doing": "I'm doing well, thanks for asking! How can I help you?",
    "what can you do": "I can answer questions, explain concepts, and chat with you. Try asking me anything!",
    "good morning": "Good morning! How can I help you today?",
    "good afternoon": "Good afternoon! What can I do for you?",
    "good evening": "Good evening! How can I assist you?",
    "thanks": "You're welcome! Anything else?",
    "thank you": "You're welcome! Happy to help.",
    "bye": "Goodbye! Come back anytime.",
    "goodbye": "Goodbye! Take care.",
}

# Mock AI: used when USE_MOCK_AI=1 or when OPENAI_API_KEY is not set
MOCK_RESPONSES = [
    "That's a great question! In a real setup, I'd use an LLM to answer. Here's a mock reply.",
    "Mock AI: I understand you're asking about \"{query}\". This is a placeholder response.",
    "Thanks for your message. (Mock mode — set OPENAI_API_KEY for real AI responses.)",
    "Mock response: I'd love to help with that. Try enabling the real API for full answers!",
]


def _normal_query_response(user_message):
    """Return predefined response for hi, hello, what is your name, etc. or None."""
    key = user_message.strip().lower().rstrip("?.!")
    if not key or len(key) > 80:
        return None
    return NORMAL_QUERIES.get(key)


def get_mock_response(user_message):
    """Return a mock reply for testing without the OpenAI API."""
    normal = _normal_query_response(user_message)
    if normal is not None:
        return normal
    template = random.choice(MOCK_RESPONSES)
    short = user_message[:50] + ("..." if len(user_message) > 50 else "")
    return template.format(query=short) if "{query}" in template else template


def get_ai_response(user_message):
    """Use OpenAI when API key is set; otherwise use Mock AI. Set USE_MOCK_AI=1 to force mock."""
    # Always answer hi/hello/etc. from NORMAL_QUERIES (no API call, no quota used)
    normal = _normal_query_response(user_message)
    if normal is not None:
        return normal

    use_mock = os.getenv("USE_MOCK_AI", "").lower() in ("1", "true", "yes")
    api_key = os.getenv("OPENAI_API_KEY")

    if use_mock or not api_key:
        return get_mock_response(user_message)

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant"},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception:
        # Quota, network, etc.: fall back to mock so the user still gets a reply
        return get_mock_response(user_message)
