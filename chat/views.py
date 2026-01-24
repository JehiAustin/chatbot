from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from .llm import get_ai_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("chat")
    else:
        form = UserCreationForm()
    return render(request, "chat/signup.html", {"form": form})

@login_required
def chat_view(request):
    print("----------- trigger")
    chats = ChatMessage.objects.filter(user=request.user)

    if request.method == "POST":
        question = request.POST["question"]
        print("USER QUESTION:", question)
        
        answer = get_ai_response(question)
        print("AI ANSWER:", answer) 

        ChatMessage.objects.create(
            user=request.user,
            question=question,
            answer=answer
        )

    return render(request, "chat/chat.html", {"chats": chats})

# @csrf_exempt  # Exempt CSRF for API calls (use cautiously; consider proper CORS setup)
# @require_http_methods(["POST"])
# def chat_api(request):
#     try:
#         data = json.loads(request.body)
#         question = data.get('question')
#         if not question:
#             return JsonResponse({'error': 'Question is required'}, status=400)
#         answer = get_ai_response(question)
#         return JsonResponse({'answer': answer})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

