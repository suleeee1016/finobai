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


class CreditAnalysisView(APIView):
    """Kredi uygunluk analizi"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            data = request.data
            
            # Gerekli alanları kontrol et
            required_fields = ['monthly_income', 'monthly_expenses', 'existing_debts']
            for field in required_fields:
                if field not in data:
                    return Response({
                        'error': f'{field} alanı zorunludur'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Kredi analiz servisini çağır
            analysis_service = CreditAnalysisService()
            analysis_result = analysis_service.analyze_credit_worthiness(
                user=request.user,
                monthly_income=Decimal(str(data['monthly_income'])),
                monthly_expenses=Decimal(str(data['monthly_expenses'])),
                existing_debts=Decimal(str(data.get('existing_debts', 0))),
                credit_score=data.get('credit_score')
            )
            
            return Response(analysis_result)
            
        except ValueError as e:
            return Response({
                'error': 'Geçersiz sayısal değer'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': f'Analiz hatası: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StockAnalysisView(APIView):
    """Borsa analizi ve tavsiyeleri"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            symbol = request.query_params.get('symbol', 'BIST100')
            
            stock_service = StockAnalysisService()
            analysis = stock_service.get_stock_analysis(symbol, request.user)
            
            return Response(analysis)
            
        except Exception as e:
            return Response({
                'error': f'Borsa analizi hatası: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            symbols = request.data.get('symbols', ['BIST100', 'USD', 'EUR', 'GOLD'])
            
            stock_service = StockAnalysisService()
            portfolio_analysis = stock_service.get_portfolio_analysis(symbols, request.user)
            
            return Response(portfolio_analysis)
            
        except Exception as e:
            return Response({
                'error': f'Portföy analizi hatası: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BudgetOptimizationView(APIView):
    """Bütçe optimizasyon tavsiyeleri"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Kullanıcının mevcut finansal verilerini al (mock data kullanacağız şimdilik)
            current_data = {
                'monthly_income': Decimal('12500'),
                'monthly_expenses': Decimal('8750'),
                'expense_categories': {
                    'market': Decimal('1925'),  # %22
                    'faturalar': Decimal('1575'),  # %18
                    'ulaşım': Decimal('875'),   # %10
                    'eğlence': Decimal('1312'),  # %15
                    'diğer': Decimal('3063')    # %35
                }
            }
            
            budget_service = BudgetOptimizationService()
            optimization = budget_service.optimize_budget(request.user, current_data)
            
            return Response(optimization)
            
        except Exception as e:
            return Response({
                'error': f'Bütçe optimizasyon hatası: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    'session_id': conv.session_id,
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
