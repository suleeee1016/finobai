import json
from decimal import Decimal
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import AIConversation, AIMessage, CreditAnalysis
from .services import FinancialAIService


class ChatBotView(APIView):
    """AI Chatbot endpoint'i - OpenAI GPT entegrasyonlu"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_message = request.data.get('message', '').strip()
            conversation_id = request.data.get('conversation_id')
            
            if not user_message:
                return Response({
                    'error': 'Mesaj boş olamaz'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Konuşmayı bul veya oluştur
            if conversation_id:
                try:
                    conversation = AIConversation.objects.get(
                        id=conversation_id,
                        user=request.user
                    )
                except AIConversation.DoesNotExist:
                    conversation = AIConversation.objects.create(user=request.user)
            else:
                conversation = AIConversation.objects.create(user=request.user)
            
            # Kullanıcı mesajını kaydet
            user_msg = AIMessage.objects.create(
                conversation=conversation,
                sender='user',
                content=user_message,
                message_type='text'
            )
            
            # AI servisini çağır (OpenAI GPT)
            ai_service = FinancialAIService()
            ai_response = ai_service.process_message(user_message, request.user)
            
            # AI cevabını kaydet
            bot_msg = AIMessage.objects.create(
                conversation=conversation,
                sender='bot',
                content=ai_response['text'],
                message_type=ai_response.get('type', 'text')
            )
            
            return Response({
                'response': ai_response['text'],
                'message_type': ai_response.get('type', 'text'),
                'conversation_id': conversation.id,
                'message_id': bot_msg.id
            })
            
        except Exception as e:
            print(f"ChatBot Error: {e}")
            return Response({
                'error': 'AI asistanına şu anda ulaşılamıyor. Lütfen daha sonra tekrar deneyin.',
                'response': f"""🤖 **Geçici Teknik Sorun**

Merhaba {request.user.first_name or 'Değerli müşteri'}!

Şu anda yapay zeka sistemimizde geçici bir sorun yaşıyoruz. Size yardımcı olmak için:

📞 **İletişim:** [email protected]
💬 **Canlı Destek:** Hafta içi 09:00-18:00
📱 **WhatsApp:** +90 XXX XXX XX XX

🏦 **Acil finansal sorularınız için:**
• Kredi başvuru rehberleri: [link]
• Borsa analizi raporları: [link]
• Bütçe planlama araçları: [link]

Anlayışınız için teşekkürler! 🙏""",
                'message_type': 'text'
            })


class ConversationHistoryView(APIView):
    """Kullanıcının AI konuşma geçmişi"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            conversations = AIConversation.objects.filter(
                user=request.user
            )[:10]  # Son 10 konuşma
            
            result = []
            for conv in conversations:
                messages = conv.messages.all()[:20]  # Son 20 mesaj
                result.append({
                    'conversation_id': conv.id,
                    'created_at': conv.created_at,
                    'updated_at': conv.updated_at,
                    'messages': [{
                        'sender': msg.sender,
                        'content': msg.content,
                        'type': msg.message_type,
                        'created_at': msg.created_at
                    } for msg in messages]
                })
            
            return Response(result)
            
        except Exception as e:
            return Response({
                'error': f'Geçmiş yüklenirken hata: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
