from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_view, name="chat"),
    path("signup/", views.signup, name="signup"),
    # path('api/chat/', views.chat_api, name='chat_api'),
]
