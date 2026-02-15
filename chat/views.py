import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .llm import get_ai_response
from .models import ChatMessage


def chat_view(request):
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            answer = get_ai_response(question)
            ChatMessage.objects.create(question=question, answer=answer)

    chats = ChatMessage.objects.all().order_by("created_at")
    return render(request, "chat/chat.html", {"chats": chats})


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()
        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)
        answer = get_ai_response(question)
        return JsonResponse({"answer": answer})
    except json.JSONDecodeError as e:
        return JsonResponse({"error": f"Invalid JSON: {e}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
