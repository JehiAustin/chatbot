"""Run sample chat queries and save them to the database."""

from django.core.management.base import BaseCommand

from chat.llm import get_ai_response
from chat.models import ChatMessage

SAMPLE_QUERIES = [
    "Hi",
    "Hello",
    "What is your name?",
    "How are you?",
    "What can you do?",
    "What is Python?",
    "How do I create a Django project?",
    "Explain REST APIs in simple terms",
    "What are the best practices for writing clean code?",
    "How does machine learning work?",
]


class Command(BaseCommand):
    help = "Run sample queries via AI and save them as ChatMessage records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing chat messages before adding samples.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            count = ChatMessage.objects.count()
            ChatMessage.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Cleared {count} existing messages."))

        for q in SAMPLE_QUERIES:
            answer = get_ai_response(q)
            ChatMessage.objects.create(question=q, answer=answer)
            preview = (answer[:60] + "...") if len(answer) > 60 else answer
            self.stdout.write(f"  {q[:50]} -> {preview}")

        self.stdout.write(self.style.SUCCESS(f"Added {len(SAMPLE_QUERIES)} sample messages."))
