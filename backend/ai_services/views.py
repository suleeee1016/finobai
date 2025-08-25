import json
from decimal import Decimal
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import AIConversation, AIMessage, CreditAnalysis
from .services import FinancialAIService


@method_decorator(csrf_exempt, name='dispatch')
class ChatBotView(APIView):
    """AI Chatbot endpoint'i - OpenAI GPT entegrasyonlu"""
    permission_classes = [AllowAny]  # Geçici olarak authentication kaldırıldı
    
    def post(self, request):
        try:
            user_message = request.data.get('message', '').strip()
            conversation_id = request.data.get('conversation_id')
            
            if not user_message:
                return Response({
                    'error': 'Mesaj boş olamaz'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Konuşmayı bul veya oluştur - Anonymous kullanıcı için sadece bellekte tut
            # Şimdilik veritabanına kaydetmiyoruz, sadece AI cevabını dönüyoruz
            
            # AI servisini çağır (OpenAI GPT)
            ai_service = FinancialAIService()
            # Anonymous user için mock user objesi
            mock_user = type('MockUser', (), {
                'first_name': 'Değerli Müşteri',
                'email': 'guest@finobai.com'
            })()
            ai_response = ai_service.process_message(user_message, mock_user)
            
            # AI cevabını kaydet - Şimdilik veritabanına kaydetmiyoruz
            
            return Response({
                'response': ai_response['text'],
                'message_type': ai_response.get('type', 'text'),
                'conversation_id': None,
                'message_id': None
            })
            
        except Exception as e:
            import traceback
            print(f"ChatBot Error: {e}")
            print(f"Full traceback: {traceback.format_exc()}")
            # Anonymous user için isim kontrolü
            user_name = 'Değerli müşteri'
            if hasattr(request.user, 'first_name') and request.user.first_name:
                user_name = request.user.first_name
            
            return Response({
                'error': 'AI asistanına şu anda ulaşılamıyor. Lütfen daha sonra tekrar deneyin.',
                'response': f"""🤖 **Geçici Teknik Sorun**

Merhaba {user_name}!

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
