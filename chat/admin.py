from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("question_preview", "answer_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("question", "answer")
    readonly_fields = ("created_at",)

    def question_preview(self, obj):
        return obj.question[:60] + "..." if len(obj.question) > 60 else obj.question

    def answer_preview(self, obj):
        return obj.answer[:60] + "..." if len(obj.answer) > 60 else obj.answer

    question_preview.short_description = "Question"
    answer_preview.short_description = "Answer"
