from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatBotView.as_view(), name='chat'),
    path('conversation-history/', views.ConversationHistoryView.as_view(), name='conversation_history'),
]
