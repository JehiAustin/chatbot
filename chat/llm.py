import os
import random

import openai

# Mock AI: used when USE_MOCK_AI=1 or when OPENAI_API_KEY is not set
MOCK_RESPONSES = [
    "That's a great question! In a real setup, I'd use an LLM to answer. Here's a mock reply.",
    "Mock AI: I understand you're asking about \"{query}\". This is a placeholder response.",
    "Thanks for your message. (Mock mode — set OPENAI_API_KEY for real AI responses.)",
    "Mock response: I'd love to help with that. Try enabling the real API for full answers!",
]


def get_mock_response(user_message):
    """Return a mock reply for testing without the OpenAI API."""
    template = random.choice(MOCK_RESPONSES)
    short = user_message[:50] + ("..." if len(user_message) > 50 else "")
    return template.format(query=short) if "{query}" in template else template


def get_ai_response(user_message):
    """Use OpenAI when API key is set; otherwise use Mock AI. Set USE_MOCK_AI=1 to force mock."""
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
    except Exception as e:
        return f"Error communicating with OpenAI: {str(e)}"
