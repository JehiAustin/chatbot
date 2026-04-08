from django.test import TestCase

from .models import ChatMessage


class ChatMessageModelTests(TestCase):
    def test_create_message(self):
        msg = ChatMessage.objects.create(
            question="Hello?",
            answer="Hi there!",
        )
        self.assertEqual(msg.question, "Hello?")
        self.assertEqual(msg.answer, "Hi there!")
        self.assertIsNotNone(msg.created_at)
