"""
OpenAI GPT entegrasyonlu finans asistanı servisleri
"""

import openai
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class FinancialAIService:
    """OpenAI GPT ile finansal AI servisi"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def process_message(self, message, user):
        """Kullanıcı mesajını GPT ile işler ve finansal tavsiye verir"""
        try:
            # Kullanıcı profil bilgilerini al
            user_context = self._get_user_context(user)
            
            # System prompt'u oluştur
            system_prompt = self._create_system_prompt(user_context)
            
            # GPT'ye gönder
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            message_type = self._determine_message_type(message)
            
            return {
                'text': ai_response,
                'type': message_type
            }
            
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return self._fallback_response(message, user)
    
    def _get_user_context(self, user):
        """Kullanıcı bağlam bilgilerini hazırla"""
        return {
            'name': user.first_name or 'Değerli müşteri',
            'email': user.email,
            'join_date': user.date_joined.strftime('%Y-%m-%d') if hasattr(user, 'date_joined') else 'Bilinmiyor'
        }
    
    def _create_system_prompt(self, user_context):
        """Sistem prompt'unu oluştur"""
        return f"""Sen Finobai adlı fintech platformunun profesyonel finansal danışmanısın. 
Türkiye'deki finansal piyasalar konusunda uzmanlaşmış, güncel ve güvenilir tavsiyelerde bulunan bir AI asistanısın.

KULLANICI BİLGİLERİ:
- İsim: {user_context['name']}
- E-posta: {user_context['email']}
- Üyelik Tarihi: {user_context['join_date']}

GÖREVİN:
🏦 Bankacılık ve krediler konusunda uzman tavsiye ver
📈 Borsa, hisse senetleri ve yatırım stratejileri öner
💰 Bütçe yönetimi ve tasarruf planları oluştur
📊 Finansal planlama ve risk yönetimi konularında rehberlik et

KURALLAR:
1. Sadece Türkçe yanıt ver
2. Emoji kullanarak görsel açıdan zengin yanıtlar oluştur
3. Güncel Türkiye finansal verilerini referans al
4. Risk uyarılarını mutlaka belirt
5. Somut, uygulanabilir tavsiyeler ver
6. Yasal sorumluluk almadığını belirt
7. Kişisel finansal durumu sorarak özelleştirilmiş tavsiye ver

YANIT FORMATI:
- Başlık (emoji ile)
- Ana analiz/tavsiye
- Somut adımlar
- Risk uyarıları
- Takip sorusu

Profesyonel ama samimi bir ton kullan. Türkiye'deki güncel ekonomik durumu dikkate al."""

    def _determine_message_type(self, message):
        """Mesaj türünü belirle"""
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in ['kredi', 'borç', 'loan']):
            return 'analysis'
        elif any(keyword in message_lower for keyword in ['borsa', 'hisse', 'yatırım', 'portföy']):
            return 'analysis'
        elif any(keyword in message_lower for keyword in ['bütçe', 'tasarruf', 'harcama']):
            return 'recommendation'
        else:
            return 'text'
    
    def _fallback_response(self, message, user):
        """OpenAI başarısız olursa yedek yanıt"""
        return {
            'text': f"""🤖 **Geçici Teknik Sorun**

Merhaba {user.first_name or 'Değerli müşteri'}!

Şu anda AI sistemimizde geçici bir teknik sorun yaşıyoruz. Ancak size yardımcı olmaya devam edebilirim:

🏦 **Bankacılık & Krediler**
• Kredi başvuru süreçleri
• Kredi karşılaştırmaları
• Borç yapılandırma

📈 **Yatırım & Borsa**
• Hisse senedi analizleri
• Portföy önerileri
• Risk değerlendirmesi

💰 **Bütçe & Tasarruf**
• Harcama planlaması
• Tasarruf stratejileri
• Mali disiplin

Lütfen sorunuzu daha spesifik olarak tekrar sorabilir misiniz? Örneğin:
"Konut kredisi almak istiyorum, ne yapmalıyım?"
"BIST 30'da hangi hisseleri önerirsiniz?"
"Aylık 5000 TL ile nasıl tasarruf yaparım?"

Teknik sorun en kısa sürede çözülecek. Anlayışınız için teşekkürler! 🙏""",
            'type': 'text'
        }


class CreditAnalysisService:
    """Kredi analiz servisi"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def analyze_credit_worthiness(self, user, monthly_income=None, monthly_expenses=None, existing_debts=0):
        """GPT ile kredi uygunluk analizi"""
        try:
            prompt = f"""Türkiye'deki bir bankanın kredi uzmanı olarak, aşağıdaki müşteri için kredi uygunluk analizi yap:

MÜŞTERI BİLGİLERİ:
- İsim: {user.first_name or 'Müşteri'}
- E-posta: {user.email}

FINANSAL DURUM:
- Aylık Gelir: {monthly_income or 'Belirtilmedi'} TL
- Aylık Gider: {monthly_expenses or 'Belirtilmedi'} TL
- Mevcut Borç: {existing_debts} TL

Lütfen şunları analiz et:
1. Kredi uygunluk skoru (0-100)
2. Risk seviyesi (düşük/orta/yüksek)
3. Önerilen kredi limiti
4. Kredi vadesi önerisi
5. Gerekli belgeler listesi
6. Kredi başvuru tavsiyeleri

Türkçe ve detaylı bir analiz yap."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'score': self._extract_score_from_response(response.choices[0].message.content),
                'risk_level': self._extract_risk_from_response(response.choices[0].message.content)
            }
            
        except Exception as e:
            print(f"Credit Analysis Error: {e}")
            return self._fallback_credit_analysis(user, monthly_income, monthly_expenses, existing_debts)
    
    def _extract_score_from_response(self, response_text):
        """GPT yanıtından skoru çıkar"""
        import re
        score_match = re.search(r'(\d+)/100|(\d+)\s*puan|skorr?\s*:?\s*(\d+)', response_text)
        if score_match:
            return int(score_match.group(1) or score_match.group(2) or score_match.group(3))
        return 75  # Varsayılan skor
    
    def _extract_risk_from_response(self, response_text):
        """GPT yanıtından risk seviyesini çıkar"""
        response_lower = response_text.lower()
        if 'düşük' in response_lower or 'low' in response_lower:
            return 'low'
        elif 'yüksek' in response_lower or 'high' in response_lower:
            return 'high'
        else:
            return 'medium'
    
    def _fallback_credit_analysis(self, user, monthly_income, monthly_expenses, existing_debts):
        """Yedek kredi analizi"""
        if monthly_income and monthly_expenses:
            net_income = monthly_income - monthly_expenses
            debt_ratio = (existing_debts / monthly_income * 100) if monthly_income > 0 else 100
            
            if net_income > 3000 and debt_ratio < 30:
                score = 85
                risk = 'low'
            elif net_income > 1500 and debt_ratio < 50:
                score = 65
                risk = 'medium'
            else:
                score = 35
                risk = 'high'
        else:
            score = 60
            risk = 'medium'
        
        return {
            'analysis': f"""🏦 **Kredi Uygunluk Analizi - {user.first_name or 'Değerli Müşteri'}**

📊 **Skorunuz:** {score}/100
⚠️ **Risk Seviyesi:** {risk}

Detaylı analiz için lütfen gelir ve gider bilgilerinizi paylaşın.""",
            'score': score,
            'risk_level': risk
        }


class StockAnalysisService:
    """Borsa analiz servisi"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def get_market_overview(self, user):
        """GPT ile güncel piyasa analizi"""
        try:
            prompt = f"""Türkiye finansal piyasalarında uzman bir analist olarak, bugün için güncel piyasa analizi yap:

GÜNCEL PIYASA ANALİZİ GEREKLİ:
1. BIST 100 durumu ve yorumu
2. Dolar/Euro kurları ve trend
3. Altın fiyatları analizi
4. Öne çıkan hisse senetleri (THYAO, AKBNK, BIMAS, EREGL, ASELS gibi)
5. Bu hafta yatırım fırsatları
6. Risk uyarıları

Türkçe, emoji kullanarak ve güncel verilerle yanıt ver.
Not: Gerçek güncel verileri kullan, varsayım yapma."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.4
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'recommendations': self._extract_stock_recommendations(response.choices[0].message.content)
            }
            
        except Exception as e:
            print(f"Stock Analysis Error: {e}")
            return self._fallback_stock_analysis()
    
    def _extract_stock_recommendations(self, response_text):
        """GPT yanıtından hisse önerilerini çıkar"""
        recommendations = []
        lines = response_text.split('\n')
        
        for line in lines:
            if any(stock in line for stock in ['THYAO', 'AKBNK', 'BIMAS', 'EREGL', 'ASELS']):
                recommendations.append(line.strip())
        
        return recommendations[:5]  # En fazla 5 öneri
    
    def _fallback_stock_analysis(self):
        """Yedek borsa analizi"""
        return {
            'analysis': """📈 **Güncel Piyasa Durumu**

⚠️ Gerçek zamanlı veri alınamadı. Genel piyasa bilgileri:

🏛️ **BIST 100:** Günlük volatilite normal seviyelerde
💱 **USD/TRY:** Merkez Bankası politikalarını takip edin
🥇 **Altın:** Güvenli liman olarak değerini koruyor

📊 **Yatırım Stratejisi:**
• Portföyünüzü çeşitlendirin
• Risk yönetimi yapın
• Uzun vadeli düşünün

💡 Güncel veriler için piyasa kaynaklarını kontrol edin.""",
            'recommendations': ['THYAO - Havayolu sektörü', 'AKBNK - Bankacılık', 'BIMAS - Perakende']
        }


class BudgetOptimizationService:
    """Bütçe optimizasyon servisi"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def optimize_budget(self, user, financial_data=None):
        """GPT ile kişiselleştirilmiş bütçe optimizasyonu"""
        try:
            prompt = f"""Türkiye'de yaşayan bir kişi için bütçe optimizasyon uzmanı olarak analiz yap:

KULLANICI: {user.first_name or 'Değerli Müşteri'}
FINANSAL VERİLER: {financial_data or 'Genel analiz talep ediliyor'}

Türkiye'deki yaşam koşulları ve ekonomik gerçekleri dikkate alarak:

1. **Bütçe Kategori Analizi**
   - Barınma (%30-35)
   - Gıda (%15-20)
   - Ulaşım (%10-15)
   - Eğlence (%5-10)
   - Tasarruf (%20-25)

2. **Somut Tasarruf Önerileri**
   - Market alışverişi ipuçları
   - Ulaşım alternatifleri  
   - Enerji tasarrufu
   - Abonelik optimizasyonu

3. **Finansal Hedefler**
   - Acil durum fonu (3-6 ay gider)
   - Yatırım planı
   - Uzun vadeli hedefler

Türkiye şartlarına uygun, uygulanabilir tavsiyeler ver."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.3
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'savings_potential': self._calculate_savings_potential(financial_data)
            }
            
        except Exception as e:
            print(f"Budget Analysis Error: {e}")
            return self._fallback_budget_analysis(user)
    
    def _calculate_savings_potential(self, financial_data):
        """Tasarruf potansiyelini hesapla"""
        if not financial_data or not isinstance(financial_data, dict):
            return {'potential_monthly_saving': 500, 'target_rate': 20}
            
        income = financial_data.get('monthly_income', 10000)
        return {
            'potential_monthly_saving': int(income * 0.05),  # %5 potansiyel tasarruf
            'target_rate': 25
        }
    
    def _fallback_budget_analysis(self, user):
        """Yedek bütçe analizi"""
        return {
            'analysis': f"""💰 **Bütçe Optimizasyon - {user.first_name or 'Değerli Müşteri'}**

📊 **Türkiye İçin Genel Bütçe Rehberi:**

🏠 **Barınma (Maksimum %35)**
• Kira/taksit + aidat + faturalar

🛒 **Market (%15-20)**
• Haftalık liste yapın
• İndirim dönemlerini takip edin
• Yerli ürünleri tercih edin

🚌 **Ulaşım (%10-15)**
• Toplu taşıma kartı kullanın
• Yürüme mesafesindeki yerleri tercih edin

💡 **Tasarruf Ipuçları:**
• Acil durum fonu oluşturun
• %20 tasarruf hedefleyin
• Aylık harcamalarınızı takip edin

Detaylı analiz için gelir/gider bilgilerinizi paylaşabilirsiniz.""",
            'savings_potential': {'potential_monthly_saving': 500, 'target_rate': 20}
        }
