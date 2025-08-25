import json
from datetime import datetime, timedelta
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from decimal import Decimal
import openai
from django.conf import settings

from .models import Expense, ExpenseCategory, Budget, ExpenseInsight


class ExpenseAnalysisService:
    """Harcama analizi ve AI önerileri servisi"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def analyze_expense_text(self, expense_text: str, amount: float) -> dict:
        """
        Harcama metnini analiz ederek kategori ve etiketleri belirler
        """
        try:
            # Önce basit keyword tabanlı kategorilendirme dene
            fallback_result = self._get_fallback_categorization(expense_text, amount)
            
            # OpenAI API ile analiz et
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Sen bir harcama analiz uzmanısın. Verilen harcama bilgisini analiz et ve şunları belirle:

Kategoriler:
- food (Gıda & İçecek)
- transport (Ulaşım) 
- entertainment (Eğlence)
- bills (Faturalar)
- shopping (Alışveriş)
- health (Sağlık)
- education (Eğitim)
- investment (Yatırım)
- housing (Konut)
- other (Diğer)

JSON formatında yanıt ver:
{
    "category": "kategori_kodu",
    "confidence": 0.95,
    "is_necessary": true/false,
    "tags": ["etiket1", "etiket2"],
    "analysis": "Kısa açıklama"
}"""
                    },
                    {
                        "role": "user",
                        "content": f"Harcama: {expense_text}, Tutar: {amount}₺"
                    }
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"OpenAI API error, using fallback: {e}")
            # OpenAI API'si çalışmıyorsa fallback kullan
            return self._get_fallback_categorization(expense_text, amount)
    
    def _get_fallback_categorization(self, expense_text: str, amount: float) -> dict:
        """Basit keyword tabanlı kategorilendirme (fallback)"""
        text_lower = expense_text.lower()
        
        # Keyword mapping
        categories = {
            'food': ['market', 'migros', 'carrefour', 'bim', 'şok', 'a101', 'restaurant', 'restoran', 
                    'yemek', 'kahve', 'cafe', 'starbucks', 'mcdonalds', 'burger', 'pizza', 'lokanta',
                    'mutfak', 'gıda', 'food', 'grocery', 'süt', 'ekmek', 'et', 'sebze', 'meyve'],
            'transport': ['benzin', 'petrol', 'shell', 'bp', 'opet', 'lukoil', 'taksi', 'uber', 
                         'bitaksi', 'otobüs', 'metro', 'dolmuş', 'araç', 'transport', 'fuel',
                         'garage', 'oto', 'servis', 'lastik', 'yağ', 'akaryakıt'],
            'entertainment': ['sinema', 'cinema', 'netflix', 'spotify', 'youtube', 'disney', 'amazon prime',
                             'eglence', 'oyun', 'game', 'konsol', 'ps5', 'xbox', 'steam', 'tiyatro',
                             'konser', 'müzik', 'film', 'kitap', 'book'],
            'bills': ['elektrik', 'su', 'doğalgaz', 'internet', 'telefon', 'vodafone', 'turkcell', 
                     'türk telekom', 'fatura', 'bill', 'abonelik', 'subscription', 'netflix',
                     'spotify', 'utilities', 'belediye', 'vergi', 'tax'],
            'shopping': ['mağaza', 'store', 'shop', 'amazon', 'trendyol', 'hepsiburada', 'gittigidiyor',
                        'zara', 'h&m', 'lcwaikiki', 'koton', 'defacto', 'mango', 'boyner',
                        'giyim', 'ayakkabı', 'çanta', 'teknoloji', 'elektronik', 'telefon', 'laptop'],
            'health': ['eczane', 'pharmacy', 'hastane', 'hospital', 'doktor', 'doctor', 'ilac', 'medicine',
                      'sağlık', 'health', 'diş', 'dental', 'göz', 'eye', 'clinic', 'klinik', 'tedavi'],
            'education': ['okul', 'school', 'kurs', 'course', 'eğitim', 'education', 'kitap', 'book',
                         'kırtasiye', 'stationery', 'university', 'üniversite', 'özel ders', 'dershane'],
            'housing': ['kira', 'rent', 'ev', 'home', 'house', 'apartman', 'site', 'housing',
                       'tamir', 'repair', 'boyama', 'paint', 'mobilya', 'furniture', 'ikea'],
            'investment': ['yatırım', 'investment', 'hisse', 'stock', 'kripto', 'crypto', 'bitcoin',
                          'borsa', 'exchange', 'fond', 'fund', 'altın', 'gold', 'döviz', 'forex']
        }
        
        # En uygun kategoriyi bul
        best_match = 'other'
        best_score = 0
        matched_keywords = []
        
        for category, keywords in categories.items():
            score = 0
            category_matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                    category_matches.append(keyword)
            
            if score > best_score:
                best_score = score
                best_match = category
                matched_keywords = category_matches
        
        # Güven skorunu hesapla
        confidence = min(0.85, 0.4 + (best_score * 0.15))
        
        # Gerekliliği belirle
        necessary_categories = ['food', 'bills', 'health', 'housing', 'transport']
        is_necessary = best_match in necessary_categories
        
        # Tutar bazlı ek kontroller
        if amount > 1000:
            confidence = min(confidence, 0.7)  # Yüksek tutarlarda daha temkinli
        
        return {
            "category": best_match,
            "confidence": confidence,
            "is_necessary": is_necessary,
            "tags": matched_keywords[:3],  # En fazla 3 tag
            "analysis": f"Otomatik olarak {best_match} kategorisine atandı (keyword match: {', '.join(matched_keywords[:2])})"
        }
    
    def get_monthly_summary(self, user: User, year: int, month: int) -> dict:
        """Aylık harcama özeti"""
        
        # O ay için tüm harcamalar
        expenses = Expense.objects.filter(
            user=user,
            expense_date__year=year,
            expense_date__month=month
        )
        
        total_spent = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # Kategori bazında analiz
        category_summary = {}
        for expense in expenses:
            cat_name = expense.category.name
            if cat_name not in category_summary:
                category_summary[cat_name] = {
                    'amount': Decimal('0'),
                    'count': 0,
                    'icon': expense.category.icon,
                    'color': expense.category.color,
                    'name': expense.category.get_name_display()
                }
            
            category_summary[cat_name]['amount'] += expense.amount
            category_summary[cat_name]['count'] += 1
        
        # En çok harcama yapılan kategori
        top_category = max(category_summary.items(), key=lambda x: x[1]['amount']) if category_summary else None
        
        # Yüzde hesapları ekle
        for cat_name, cat_data in category_summary.items():
            cat_data['percentage'] = float((cat_data['amount'] / total_spent) * 100) if total_spent > 0 else 0
        
        return {
            'total_spent': float(total_spent),
            'expense_count': expenses.count(),
            'category_summary': category_summary,
            'top_category': top_category[0] if top_category else None,
            'top_category_amount': float(top_category[1]['amount']) if top_category else 0,
            'average_per_day': float(total_spent / 30),
            'month': month,
            'year': year
        }
    
    def generate_insights(self, user: User) -> list:
        """Kullanıcı için harcama içgörüleri üretir"""
        
        insights = []
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        # Bu ayın verileri
        current_summary = self.get_monthly_summary(user, current_year, current_month)
        
        # Geçen ayın verileri (karşılaştırma için)
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        prev_summary = self.get_monthly_summary(user, prev_year, prev_month)
        
        # 1. Bütçe aşımı kontrolü
        budgets = Budget.objects.filter(user=user, month=current_month, year=current_year)
        for budget in budgets:
            if budget.budget_percentage_used > 80:
                insight_type = 'warning' if budget.budget_percentage_used > 100 else 'warning'
                insights.append({
                    'type': insight_type,
                    'title': f"{budget.category.get_name_display()} Bütçesi",
                    'message': f"Bu ay {budget.category.get_name_display()} kategorisinde bütçenizin %{budget.budget_percentage_used:.1f}'ini kullandınız. Kalan: {budget.remaining_budget}₺",
                    'priority': 5 if budget.budget_percentage_used > 100 else 3,
                    'category': budget.category.name
                })
        
        # 2. Geçen ayla karşılaştırma
        if prev_summary['total_spent'] > 0:
            change_percent = ((current_summary['total_spent'] - prev_summary['total_spent']) / prev_summary['total_spent']) * 100
            
            if abs(change_percent) > 20:  # %20'den fazla değişim varsa
                insight_type = 'warning' if change_percent > 0 else 'achievement'
                direction = 'arttı' if change_percent > 0 else 'azaldı'
                insights.append({
                    'type': insight_type,
                    'title': 'Aylık Harcama Trendi',
                    'message': f"Bu ay toplam harcamanız geçen aya göre %{abs(change_percent):.1f} {direction}. Toplam: {current_summary['total_spent']:.2f}₺",
                    'priority': 2,
                    'category': None
                })
        
        # 3. En çok harcama yapılan kategori analizi
        if current_summary['top_category']:
            top_cat = current_summary['category_summary'][current_summary['top_category']]
            insights.append({
                'type': 'trend',
                'title': 'En Çok Harcama Kategoriniz',
                'message': f"Bu ay en çok {top_cat['name']} kategorisinde harcama yaptınız: {top_cat['amount']:.2f}₺ ({top_cat['count']} işlem)",
                'priority': 1,
                'category': current_summary['top_category']
            })
        
        return insights
    
    def get_expense_recommendations(self, user: User, expense_text: str, amount: float) -> str:
        """Harcama için AI önerisi üretir"""
        
        # Kullanıcının son 30 günlük harcama patterns
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_expenses = Expense.objects.filter(
            user=user,
            expense_date__gte=thirty_days_ago
        )
        
        # Kategori bazında toplam harcamalar
        category_totals = {}
        for expense in recent_expenses:
            cat = expense.category.name
            if cat not in category_totals:
                category_totals[cat] = 0
            category_totals[cat] += float(expense.amount)
        
        context = f"""
        Kullanıcının son 30 günlük harcama özeti:
        {json.dumps(category_totals, indent=2)}
        
        Yeni harcama: {expense_text} - {amount}₺
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Sen bir kişisel finans uzmanısın. Kullanıcının harcama alışkanlıklarını analiz ederek Türkçe tavsiyeler ver. Kısa ve pratik öneriler sun."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Bu harcamanız {expense_text} kategorisinde kaydedildi. Bütçenizi takip etmeye devam edin! 💡"
