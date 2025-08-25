"""
Basit AI servisleri - Type annotation'sız
"""

import random
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()


class FinancialAIService:
    """Ana AI servisi"""
    
    def process_message(self, message, user):
        """Mesajı işler ve uygun cevabı döner"""
        message_lower = message.lower()
        
        # Kredi sorularını tespit et
        if any(keyword in message_lower for keyword in ['kredi', 'loan', 'borç']):
            return self._handle_credit_query(user)
        
        # Borsa sorularını tespit et
        elif any(keyword in message_lower for keyword in ['borsa', 'hisse', 'yatırım']):
            return self._handle_stock_query(user)
        
        # Bütçe sorularını tespit et
        elif any(keyword in message_lower for keyword in ['bütçe', 'harcama', 'tasarruf']):
            return self._handle_budget_query(user)
        
        # Genel cevap
        else:
            return self._handle_general_query(user)
    
    def _handle_credit_query(self, user):
        """Kredi analizi cevabı"""
        return {
            'text': f"""🏦 **Kredi Uygunluk Analizi**

📊 **Mevcut Finansal Durumunuz:**
• Aylık Gelir: ₺12.500
• Aylık Gider: ₺8.750
• Net Tasarruf: ₺3.750
• Borç/Gelir Oranı: %12 (İdeal: <%30)

✅ **Kredi Uygunluğu: YÜKSEK**

💰 **Önerilen Kredi Limitleri:**
• Konut Kredisi: ₺850.000 (120 ay)
• İhtiyaç Kredisi: ₺150.000 (36 ay)
• Araç Kredisi: ₺400.000 (60 ay)

📋 **Gerekli Belgeler:**
• Kimlik fotokopisi
• Son 3 ay maaş bordrosu
• SGK hizmet dökümü
• İkametgah belgesi

💡 **Önerilerim:**
1. Mevcut borçlarınızı kapatın
2. 3 ay daha tasarruf yapın
3. Kredi notu raporunu kontrol edin

Hangi tür kredi için başvuru yapmayı planlıyorsunuz?""",
            'type': 'analysis'
        }
    
    def _handle_stock_query(self, user):
        """Borsa analizi cevabı"""
        return {
            'text': f"""📈 **Borsa ve Yatırım Analizi**

📊 **Güncel Piyasa Durumu:**
• BIST 100: 9.847 (+%1.2)
• USD/TRY: 28.45 (-%0.3)
• EUR/TRY: 31.22 (+%0.1)
• Altın: ₺2.847/gr (+%0.8)

🎯 **Size Özel Öneriler:**
• **Risk Profili:** Orta seviye
• **Yatırım Ufku:** 2-5 yıl
• **Portföy Önerisi:** %40 Hisse, %30 Tahvil, %20 Altın, %10 Döviz

📈 **Bu Hafta Öne Çıkanlar:**
1. **THYAO** - Türk Hava Yolları (+%8.5)
2. **AKBNK** - Akbank (+%3.2)  
3. **BIMAS** - BİM (+%2.1)

⚠️ **Risk Uyarıları:**
• Yüksek volatilite bekleniyor
• Jeopolitik riskler mevcut
• Sadece kaybetmeyi göze alabileceğiniz miktarı yatırın

💡 **Strateji:**
Aylık ₺500-1000 sistematik yatırım planı başlatın.

Hangi sektör hakkında daha detaylı bilgi istiyorsunuz?""",
            'type': 'analysis'
        }
    
    def _handle_budget_query(self, user):
        """Bütçe analizi cevabı"""
        return {
            'text': f"""💰 **Bütçe Optimizasyon Analizi**

📊 **Bu Ay Finansal Özet:**
• Toplam Gelir: ₺12.500
• Toplam Gider: ₺8.750
• Tasarruf Oranı: %30 (Hedef: %20)
• En Yüksek Kategori: Market (%22)

✅ **Güçlü Yönler:**
• Tasarruf hedefini aştınız!
• Sabit giderler kontrol altında
• Düzenli gelir akışı var

⚠️ **İyileştirme Alanları:**
• Dışarıda yemek harcamaları yüksek
• Eğlence bütçesi %15 aşılmış
• Acil durum fonu 3 aya çıkarılmalı

📈 **Optimizasyon Önerileri:**
1. **Market:** Haftalık liste yapın (-₺200/ay)
2. **Abonelikler:** Kullanmadıklarını iptal edin (-₺150/ay)
3. **Ulaşım:** Toplu taşıma kullanın (-₺180/ay)

🎯 **Hedef:** Aylık ₺500 ek tasarruf

Hangi kategori hakkında detaylı analiz istiyorsunuz?""",
            'type': 'recommendation'
        }
    
    def _handle_general_query(self, user):
        """Genel finansal tavsiye"""
        return {
            'text': f"""💡 **Genel Finansal Tavsiye**

Merhaba {user.first_name}! Size şu konularda yardımcı olabilirim:

🏦 **Bankacılık & Krediler**
• Kredi uygunluk analizi
• En uygun kredi karşılaştırması
• Kredi notu iyileştirme
• Mortgage hesaplama

📈 **Yatırım & Borsa**
• Portföy analizi
• Hisse senedi tavsiyeleri
• Risk yönetimi
• Piyasa yorumları

💰 **Bütçe & Tasarruf**
• Harcama analizi
• Tasarruf planları
• Kategori optimizasyonu
• Hedef belirleme

📊 **Finansal Planlama**
• Emeklilik planlaması
• Acil durum fonu
• Sigortacılık
• Vergi optimizasyonu

Hangi konuda yardıma ihtiyacınız var? Örneğin:
• "Kredi almaya uygun muyum?"
• "Hangi hisse senedine yatırım yapmalıyım?"
• "Bütçemi nasıl optimize ederim?"

Spesifik sorularınızı bekliyorum! 😊""",
            'type': 'text'
        }


class CreditAnalysisService:
    """Kredi analiz servisi"""
    
    def analyze_credit_worthiness(self, user, monthly_income, monthly_expenses, existing_debts=0):
        """Basit kredi analizi"""
        net_income = monthly_income - monthly_expenses
        debt_ratio = (existing_debts / monthly_income * 100) if monthly_income > 0 else 100
        
        # Basit skorlama
        if net_income > 3000 and debt_ratio < 30:
            score = 85
            risk = 'low'
            max_loan = net_income * 60  # 60 aylık
        elif net_income > 1500 and debt_ratio < 50:
            score = 65  
            risk = 'medium'
            max_loan = net_income * 48
        else:
            score = 35
            risk = 'high'
            max_loan = net_income * 24
            
        return {
            'score': score,
            'risk_level': risk,
            'max_loan_amount': float(max_loan),
            'recommended_term': 60 if risk == 'low' else 48 if risk == 'medium' else 24
        }


class StockAnalysisService:
    """Borsa analiz servisi"""
    
    def get_market_overview(self, user):
        """Piyasa özeti"""
        return {
            'market_data': {
                'BIST100': {'price': 9847, 'change': 1.2},
                'USD/TRY': {'price': 28.45, 'change': -0.3},
                'EUR/TRY': {'price': 31.22, 'change': 0.1},
                'GOLD': {'price': 2847, 'change': 0.8}
            },
            'recommendations': [
                {'symbol': 'THYAO', 'name': 'Türk Hava Yolları', 'change': 8.5},
                {'symbol': 'AKBNK', 'name': 'Akbank', 'change': 3.2},
                {'symbol': 'BIMAS', 'name': 'BİM', 'change': 2.1}
            ]
        }


class BudgetOptimizationService:
    """Bütçe optimizasyon servisi"""
    
    def optimize_budget(self, user, financial_data):
        """Bütçe optimizasyon önerileri"""
        income = financial_data['monthly_income']
        expenses = financial_data['monthly_expenses']
        current_savings = income - expenses
        current_rate = (current_savings / income * 100) if income > 0 else 0
        
        # Basit optimizasyon önerileri
        optimizations = [
            {
                'category': 'Market Alışverişi',
                'current_amount': float(income * Decimal('0.22')),  # %22 varsayım
                'potential_saving': float(income * Decimal('0.03')),  # %3 tasarruf
                'suggestions': [
                    'Haftalık alışveriş listesi yapın',
                    'Discount marketleri tercih edin',
                    'Mevsimine uygun ürünler alın'
                ]
            },
            {
                'category': 'Eğlence',
                'current_amount': float(income * Decimal('0.15')),
                'potential_saving': float(income * Decimal('0.05')),
                'suggestions': [
                    'Ev partileri organize edin',
                    'Ücretsiz etkinlikleri tercih edin',
                    'Streaming aboneliklerini gözden geçirin'
                ]
            }
        ]
        
        return {
            'current_savings_rate': current_rate,
            'target_savings_rate': min(35.0, current_rate + 5),
            'optimizations': optimizations,
            'detailed_report': f"Mevcut tasarruf oranınız %{current_rate:.1f}. Hedef: %{min(35, current_rate + 5):.1f}"
        }
