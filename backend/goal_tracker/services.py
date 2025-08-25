import openai
from openai import OpenAI
from django.conf import settings
from .models import FinancialGoal, GoalContribution
from .goal_specific_analysis import GoalSpecificAnalyzer
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import json


class GoalAnalysisService:
    """AI destekli hedef analiz servisi"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def analyze_personal_goals(self, user_id):
        """Kullanıcının kişisel hedeflerine yönelik detaylı analiz"""
        try:
            from django.contrib.auth.models import User
            from expense_tracker.models import Expense
            
            user = User.objects.get(id=user_id)
            user_goals = FinancialGoal.objects.filter(user_id=user_id, is_active=True)
            
            # Kullanıcının harcama verilerini al (son 6 ay)
            six_months_ago = timezone.now() - timedelta(days=180)
            expenses = Expense.objects.filter(
                user_id=user_id,
                expense_date__gte=six_months_ago
            )
            
            # Detaylı analizler
            expense_analysis = self._analyze_user_expenses_detailed(expenses)
            goal_analysis = self._analyze_user_goals_detailed(user_goals)
            compatibility_analysis = self._analyze_goal_expense_compatibility(user_goals, expenses)
            
            # Kişiselleştirilmiş analiz promptu
            prompt = f"""
            {user.first_name or user.username} kullanıcısının KAPSAMLI kişisel finansal analizi:

            🎯 HEDEF ANALİZİ:
            - Toplam hedef sayısı: {goal_analysis['total_goals']}
            - Toplam hedef tutarı: ₺{goal_analysis['total_target_amount']:,.2f}
            - Ortalama hedef büyüklüğü: ₺{goal_analysis['avg_goal_size']:,.2f}
            - Yüksek öncelikli hedefler: {goal_analysis['high_priority_count']}
            - En büyük hedef: {goal_analysis['largest_goal']['name']} (₺{goal_analysis['largest_goal']['amount']:,.2f})
            - Kategoriler: {', '.join(goal_analysis['categories'])}
            - Toplam ilerleme: %{goal_analysis['total_progress']:.1f}

            💸 HARCAMA ANALİZİ (Son 6 ay):
            - Toplam harcama: ₺{expense_analysis['total_expense']:,.2f}
            - Aylık ortalama: ₺{expense_analysis['monthly_average']:,.2f}
            - Günlük ortalama: ₺{expense_analysis['daily_average']:,.2f}
            - En çok harcanan kategori: {expense_analysis['top_category']} (₺{expense_analysis['top_amount']:,.2f})
            - Harcama çeşitliliği: {expense_analysis['category_count']} kategori
            - Büyük harcamalar (>₺500): {expense_analysis['big_expenses_count']} adet

            🔗 UYUMLULUK ANALİZİ:
            - Hedef-harcama uyumu: {compatibility_analysis['compatibility_score']}/10
            - Tasarruf potansiyeli: ₺{compatibility_analysis['saving_potential']:,.2f}/ay
            - Riskli harcama kategorileri: {', '.join(compatibility_analysis['risky_categories'])}
            - Hedef gerçekleşme süresi: {compatibility_analysis['realistic_timeline']}

            Bu VERİLERE DAYANARAK, lütfen şu konularda DETAYLI ve KİŞİSELLEŞTİRİLMİŞ analiz yap:

            1. KİŞİNİN HEDEF STRATEJİSİ DEĞERLENDİRMESİ
            2. HARCAMA DESENLERİNİN HEDEFLERİ ETKİSİ
            3. GERÇEKÇİ ZAMAN ÇİZELGESİ ve ÖNCELİK SIRALAMA
            4. SOMUT TASARRUF STRATEJİLERİ
            5. AYLIK AKSIYON PLANI

            JSON formatında Türkçe cevap ver:
            {{
                "kisisel_durum": {{
                    "finansal_saglik_skoru": 85,
                    "hedef_stratejisi": "dengeli|agresif|muhafazakar",
                    "tasarruf_kapasitesi": "yüksek|orta|düşük",
                    "risk_profili": "düşük|orta|yüksek",
                    "genel_degerlendirme": "detaylı açıklama"
                }},
                "hedef_analizi": {{
                    "en_onemli_hedef": "hedef adı",
                    "ilk_odaklanilmasi_gereken": "hedef adı",
                    "hedef_siralama_onerisi": ["hedef1", "hedef2", "hedef3"],
                    "gecersiz_timeline": "12-18 ay gibi"
                }},
                "harcama_optimizasyonu": {{
                    "kesinti_yapilabilir_kategoriler": [
                        {{"kategori": "eğlence", "mevcut": 600, "hedef": 400, "tasarruf": 200}}
                    ],
                    "aylık_tasarruf_potansiyeli": 800,
                    "kritik_harcamalar": ["kategori1", "kategori2"]
                }},
                "eylem_plani": [
                    {{
                        "ay": 1,
                        "hedefler": ["hedef1 için ₺X", "hedef2 için ₺Y"],
                        "harcama_hedefleri": {{"kategori": "yeni_limit"}},
                        "odak": "ana görev"
                    }}
                ],
                "motivasyon_onerileri": [
                    "kişiselleştirilmiş motivasyon önerisi 1",
                    "kişiselleştirilmiş motivasyon önerisi 2"
                ],
                "risk_uyarilari": [
                    "potansiyel risk 1",
                    "potansiyel risk 2"
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen uzman bir kişisel finans danışmanısın. Kullanıcının gerçek verilerine dayanarak, kişiye özel, uygulanabilir ve motivasyon verici finansal stratejiler geliştiriyorsun. Türkçe konuşuyorsun ve her tavsiyeni verilerle destekliyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.6
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'analysis': analysis,
                'data_summary': {
                    'goals': goal_analysis,
                    'expenses': expense_analysis,
                    'compatibility': compatibility_analysis
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_goal_progress(self, goal_id):
        """Hedef ilerleme analizi"""
        try:
            goal = FinancialGoal.objects.get(id=goal_id)
            
            # Hedef verilerini topla
            goal_data = self._prepare_goal_data(goal)
            
            prompt = f"""
            Finansal hedef analizi yap:
            
            Hedef: {goal_data['name']}
            Kategori: {goal_data['category']}
            Hedef Tutar: ₺{goal_data['target_amount']:,.2f}
            Mevcut Tutar: ₺{goal_data['current_amount']:,.2f}
            İlerleme: %{goal_data['progress']:.1f}
            Kalan Süre: {goal_data['months_remaining']} ay
            Aylık Katkı: ₺{goal_data['monthly_contribution']:,.2f}
            Gerekli Aylık Tutar: ₺{goal_data['required_monthly']:,.2f}
            
            Son 30 günde {goal_data['recent_contributions']} katkı yapılmış.
            
            Lütfen şu konularda analiz yap:
            1. Mevcut ilerleme durumu
            2. Hedefin gerçekleştirilebilirlik durumu
            3. Öneriler ve iyileştirmeler
            4. Risk faktörleri
            
            Cevabını JSON formatında ver:
            {{
                "progress_analysis": "analiz metni",
                "feasibility": "çok kolay|kolay|orta|zor|çok zor",
                "recommendations": ["öneri1", "öneri2", ...],
                "risk_factors": ["risk1", "risk2", ...],
                "monthly_adjustment": rakam (eğer aylık katkı artırılması gerekiyorsa)
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen uzman bir finansal danışmansın. Türkçe ve anlaşılır cevaplar veriyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'analysis': analysis
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_goal_recommendations(self, user_id):
        """Kullanıcı için genel hedef önerileri"""
        try:
            user_goals = FinancialGoal.objects.filter(user_id=user_id, is_active=True)
            
            # Kullanıcı profilini çıkar
            profile_data = self._analyze_user_profile(user_goals)
            
            prompt = f"""
            Kullanıcı finansal profili:
            
            Aktif Hedef Sayısı: {profile_data['active_goals']}
            Toplam Hedef Tutarı: ₺{profile_data['total_target']:,.2f}
            Toplam Biriken: ₺{profile_data['total_saved']:,.2f}
            Ortalama İlerleme: %{profile_data['avg_progress']:.1f}
            Hedef Kategorileri: {', '.join(profile_data['categories'])}
            Aylık Toplam Katkı: ₺{profile_data['monthly_contribution']:,.2f}
            
            Bu profile göre:
            1. Yeni hedef önerileri
            2. Mevcut hedeflerin iyileştirilmesi
            3. Finansal planlama stratejileri
            4. Risk yönetimi önerileri
            
            JSON formatında cevap ver:
            {{
                "new_goal_suggestions": [
                    {{"category": "kategori", "name": "hedef adı", "estimated_amount": rakam, "priority": "yüksek|orta|düşük"}}
                ],
                "improvement_suggestions": ["iyileştirme1", "iyileştirme2", ...],
                "strategy_recommendations": ["strateji1", "strateji2", ...],
                "risk_management": ["risk yönetimi1", "risk yönetimi2", ...]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen uzman bir finansal planlama danışmanısın. Türkçe ve pratik öneriler veriyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.8
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'recommendations': recommendations
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_contribution_patterns(self, goal_id, timeframe='3m'):
        """Katkı paternlerini analiz et"""
        try:
            goal = FinancialGoal.objects.get(id=goal_id)
            
            # Zaman aralığını belirle
            if timeframe == '1m':
                start_date = timezone.now() - timedelta(days=30)
            elif timeframe == '3m':
                start_date = timezone.now() - timedelta(days=90)
            elif timeframe == '6m':
                start_date = timezone.now() - timedelta(days=180)
            else:  # 1y
                start_date = timezone.now() - timedelta(days=365)
            
            contributions = GoalContribution.objects.filter(
                goal=goal,
                date__gte=start_date
            ).order_by('date')
            
            # Pattern analizi için veri hazırla
            pattern_data = self._analyze_contribution_patterns(contributions)
            
            prompt = f"""
            {timeframe} dönemindeki katkı paterni analizi:
            
            Toplam Katkı: ₺{pattern_data['total_amount']:,.2f}
            Katkı Sayısı: {pattern_data['contribution_count']}
            Ortalama Katkı: ₺{pattern_data['avg_amount']:,.2f}
            En Yüksek Katkı: ₺{pattern_data['max_amount']:,.2f}
            En Düşük Katkı: ₺{pattern_data['min_amount']:,.2f}
            Düzenlilik Skoru: {pattern_data['regularity_score']}/10
            Kaynak Dağılımı: {pattern_data['source_distribution']}
            
            Bu verilere göre:
            1. Katkı paterninin değerlendirmesi
            2. Düzenlilik analizi
            3. İyileştirme önerileri
            4. Gelecek dönem tahminleri
            
            JSON formatında cevap ver:
            {{
                "pattern_analysis": "analiz metni",
                "regularity_rating": "çok iyi|iyi|orta|zayıf|çok zayıf",
                "improvement_tips": ["öneri1", "öneri2", ...],
                "future_predictions": {{
                    "next_month_estimate": rakam,
                    "goal_completion_date": "YYYY-MM-DD tahmini"
                }}
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen uzman bir finansal analiz uzmanısın. Türkçe ve detaylı analizler yapıyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.6
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'analysis': analysis,
                'pattern_data': pattern_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _prepare_goal_data(self, goal):
        """Hedef verilerini analiz için hazırla"""
        recent_contributions = GoalContribution.objects.filter(
            goal=goal,
            date__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        return {
            'name': goal.name,
            'category': goal.get_category_display(),
            'target_amount': float(goal.target_amount),
            'current_amount': float(goal.current_amount),
            'progress': float(goal.progress_percentage),
            'months_remaining': goal.months_remaining,
            'monthly_contribution': float(goal.monthly_contribution),
            'required_monthly': float(goal.required_monthly_amount),
            'recent_contributions': recent_contributions
        }
    
    def _analyze_user_profile(self, goals):
        """Kullanıcı profilini analiz et"""
        total_target = sum(goal.target_amount for goal in goals)
        total_saved = sum(goal.current_amount for goal in goals)
        avg_progress = sum(goal.progress_percentage for goal in goals) / len(goals) if goals else 0
        categories = list(set(goal.get_category_display() for goal in goals))
        monthly_contribution = sum(goal.monthly_contribution for goal in goals)
        
        return {
            'active_goals': goals.count(),
            'total_target': float(total_target),
            'total_saved': float(total_saved),
            'avg_progress': float(avg_progress),
            'categories': categories,
            'monthly_contribution': float(monthly_contribution)
        }
    
    def _analyze_contribution_patterns(self, contributions):
        """Katkı paternlerini analiz et"""
        if not contributions:
            return {
                'total_amount': 0,
                'contribution_count': 0,
                'avg_amount': 0,
                'max_amount': 0,
                'min_amount': 0,
                'regularity_score': 0,
                'source_distribution': {}
            }
        
        amounts = [float(c.amount) for c in contributions]
        sources = [c.source for c in contributions]
        
        # Kaynak dağılımı
        source_dist = {}
        for source in sources:
            source_dist[source] = source_dist.get(source, 0) + 1
        
        # Düzenlilik skoru (basit hesaplama)
        regularity_score = min(10, len(contributions) // 2)
        
        return {
            'total_amount': sum(amounts),
            'contribution_count': len(contributions),
            'avg_amount': sum(amounts) / len(amounts),
            'max_amount': max(amounts),
            'min_amount': min(amounts),
            'regularity_score': regularity_score,
            'source_distribution': source_dist
        }
    
    def _analyze_user_expenses_detailed(self, expenses):
        """Kullanıcının harcama verilerini detaylı analiz et"""
        if not expenses.exists():
            return {
                'total_expense': 0,
                'monthly_average': 0,
                'daily_average': 0,
                'top_category': 'Veri yok',
                'top_amount': 0,
                'category_count': 0,
                'big_expenses_count': 0,
                'trend': 'Veri yok'
            }
        
        total = sum(float(expense.amount) for expense in expenses)
        monthly_avg = total / 6  # Son 6 ay
        daily_avg = total / 180  # Son 180 gün
        
        # Kategori analizi
        categories = {}
        for expense in expenses:
            cat = expense.category.name
            categories[cat] = categories.get(cat, 0) + float(expense.amount)
        
        top_category = max(categories.items(), key=lambda x: x[1]) if categories else ('Belirtilmemiş', 0)
        
        # Büyük harcamalar (>500₺)
        big_expenses = [e for e in expenses if float(e.amount) > 500]
        
        return {
            'total_expense': total,
            'monthly_average': monthly_avg,
            'daily_average': daily_avg,
            'top_category': top_category[0],
            'top_amount': top_category[1],
            'category_count': len(categories),
            'big_expenses_count': len(big_expenses),
            'trend': self._calculate_expense_trend(expenses)
        }
    
    def _analyze_user_goals_detailed(self, goals):
        """Kullanıcının hedeflerini detaylı analiz et"""
        if not goals.exists():
            return {
                'total_goals': 0,
                'total_target_amount': 0,
                'avg_goal_size': 0,
                'high_priority_count': 0,
                'largest_goal': {'name': 'Yok', 'amount': 0},
                'categories': [],
                'total_progress': 0
            }
        
        goals_list = list(goals)
        total_target = sum(float(goal.target_amount) for goal in goals_list)
        avg_goal_size = total_target / len(goals_list)
        high_priority = [g for g in goals_list if g.priority == 1]
        largest_goal = max(goals_list, key=lambda g: g.target_amount)
        categories = list(set(goal.category for goal in goals_list))
        total_progress = sum(goal.progress_percentage for goal in goals_list) / len(goals_list)
        
        return {
            'total_goals': len(goals_list),
            'total_target_amount': total_target,
            'avg_goal_size': avg_goal_size,
            'high_priority_count': len(high_priority),
            'largest_goal': {'name': largest_goal.name, 'amount': float(largest_goal.target_amount)},
            'categories': categories,
            'total_progress': total_progress
        }
    
    def _analyze_goal_expense_compatibility(self, goals, expenses):
        """Hedefler ve harcamalar arasındaki uyumluluğu analiz et"""
        if not goals.exists() or not expenses.exists():
            return {
                'compatibility_score': 5,
                'saving_potential': 0,
                'risky_categories': [],
                'realistic_timeline': 'Belirlenemedi'
            }
        
        monthly_expense = sum(float(e.amount) for e in expenses) / 6
        total_target = sum(float(g.target_amount) for g in goals)
        monthly_goal_need = total_target / 24  # 2 yıl hedef
        
        # Uyumluluk skoru (0-10)
        if monthly_expense < monthly_goal_need:
            compatibility_score = 9  # Çok iyi
        elif monthly_expense < monthly_goal_need * 1.5:
            compatibility_score = 7  # İyi
        elif monthly_expense < monthly_goal_need * 2:
            compatibility_score = 5  # Orta
        else:
            compatibility_score = 3  # Düşük
        
        # Tasarruf potansiyeli
        saving_potential = max(0, monthly_expense * 0.2)  # %20 tasarruf potansiyeli
        
        # Riskli kategoriler (fazla harcanan)
        expense_categories = {}
        for expense in expenses:
            cat = expense.category.name
            expense_categories[cat] = expense_categories.get(cat, 0) + float(expense.amount)
        
        monthly_categories = {k: v/6 for k, v in expense_categories.items()}
        risky_categories = [cat for cat, amount in monthly_categories.items() 
                          if amount > 500 and cat in ['Eğlence', 'Giyim']]
        
        # Gerçekçi zaman çizelgesi
        if saving_potential > 0:
            months_needed = total_target / saving_potential
            if months_needed <= 12:
                realistic_timeline = f"{int(months_needed)} ay"
            elif months_needed <= 36:
                realistic_timeline = f"{int(months_needed/12)} yıl"
            else:
                realistic_timeline = "3+ yıl"
        else:
            realistic_timeline = "Mevcut durumda ulaşılamaz"
        
        return {
            'compatibility_score': compatibility_score,
            'saving_potential': saving_potential,
            'risky_categories': risky_categories,
            'realistic_timeline': realistic_timeline
        }
    
    def _calculate_expense_trend(self, expenses):
        """Harcama trendini hesapla"""
        if not expenses.exists():
            return 'Veri yok'
        
        # Son 3 ay vs önceki 3 ay karşılaştırması
        now = timezone.now()
        three_months_ago = now - timedelta(days=90)
        
        recent_expenses = [e for e in expenses if e.expense_date >= three_months_ago]
        older_expenses = [e for e in expenses if e.expense_date < three_months_ago]
        
        if not older_expenses:
            return 'Yetersiz veri'
        
        recent_total = sum(float(e.amount) for e in recent_expenses)
        older_total = sum(float(e.amount) for e in older_expenses)
        
        if recent_total > older_total * 1.1:
            return 'Artış trendi'
        elif recent_total < older_total * 0.9:
            return 'Azalış trendi'
        else:
            return 'Sabit trend'
    
    def _generate_goal_specific_recommendations(self, user_goals, goal_specific_analyses, expenses):
        """Her hedef için spesifik öneriler oluştur"""
        recommendations = []
        
        for goal in user_goals:
            if goal.id in goal_specific_analyses:
                analysis = goal_specific_analyses[goal.id]
                recs = analysis.get('specific_recommendations', [])
                for rec in recs:
                    recommendations.append(f"[{goal.name}] {rec}")
        
        return '\n'.join(recommendations)
    
    def _format_goal_specific_analyses_for_prompt(self, goal_specific_analyses):
        """Hedef-spesifik analizleri prompt formatında hazırla"""
        formatted_analyses = []
        
        for goal_id, analysis in goal_specific_analyses.items():
            goal_info = f"""
            Hedef: {analysis.get('goal_name', 'N/A')}
            Kategori: {analysis.get('goal_category', 'N/A')}  
            Strateji Tipi: {analysis.get('strategy_type', 'N/A')}
            Gerçekleşebilirlik Skoru: {analysis.get('feasibility_score', 'N/A')}/100
            Öncelik Seviyesi: {analysis.get('priority_level', 'N/A')}
            Aylık Hedef: ₺{analysis.get('monthly_target_needed', 0):,.0f}
            """
            formatted_analyses.append(goal_info.strip())
        
        return '\n'.join(formatted_analyses)


class GoalPlanningService:
    """Hedef planlama ve optimizasyon servisi"""
    
    def calculate_optimal_savings_plan(self, goals_data):
        """Çoklu hedef için optimal tasarruf planı hesapla"""
        try:
            # Hedefleri öncelik ve tarihe göre sırala
            sorted_goals = sorted(goals_data, key=lambda x: (x['priority'], x['target_date']))
            
            total_monthly_budget = sum(goal['monthly_contribution'] for goal in goals_data)
            
            # Her hedef için optimal katkı miktarını hesapla
            optimized_plan = []
            
            for goal in sorted_goals:
                months_remaining = self._calculate_months_between(date.today(), goal['target_date'])
                required_monthly = goal['remaining_amount'] / max(months_remaining, 1)
                
                # Mevcut katkı ile gerekli katkıyı karşılaştır
                adjustment_needed = required_monthly - goal['monthly_contribution']
                
                optimized_plan.append({
                    'goal_id': goal['id'],
                    'goal_name': goal['name'],
                    'current_monthly': goal['monthly_contribution'],
                    'required_monthly': required_monthly,
                    'adjustment_needed': adjustment_needed,
                    'feasibility': 'possible' if adjustment_needed <= 0 else 'needs_adjustment'
                })
            
            return {
                'success': True,
                'optimized_plan': optimized_plan,
                'total_monthly_needed': sum(plan['required_monthly'] for plan in optimized_plan),
                'total_current_budget': total_monthly_budget
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_months_between(self, start_date, end_date):
        """İki tarih arasındaki ay farkını hesapla"""
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    
    def analyze_personal_goals(self, user_id):
        """Kullanıcının kişisel hedeflerine yönelik detaylı analiz - ENHANCED VERSION"""
        try:
            from django.contrib.auth.models import User
            from expense_tracker.models import Expense
            
            user = User.objects.get(id=user_id)
            user_goals = FinancialGoal.objects.filter(user_id=user_id, is_active=True)
            
            # Kullanıcının harcama verilerini al (son 6 ay)
            six_months_ago = timezone.now() - timedelta(days=180)
            expenses = Expense.objects.filter(
                user_id=user_id,
                expense_date__gte=six_months_ago
            )
            
            # YENİ: Hedef-spesifik analiz sistemi
            goal_specific_analyzer = GoalSpecificAnalyzer()
            
            # Her hedef için spesifik analiz
            goal_specific_analyses = {}
            for goal in user_goals:
                user_profile = {
                    'age': getattr(user, 'age', 30),  # Default age
                    'risk_tolerance': 'medium',
                    'income_stability': 'stable'
                }
                goal_specific_analyses[goal.id] = goal_specific_analyzer.analyze_goal_specifically(
                    goal, expenses, user_profile
                )
            
            # Detaylı analizler (mevcut sistem)
            expense_analysis = self._analyze_user_expenses_detailed(expenses)
            goal_analysis = self._analyze_user_goals_detailed(user_goals)
            compatibility_analysis = self._analyze_goal_expense_compatibility(user_goals, expenses)
            
            # ENHANCED: Hedef-spesifik öneriler oluştur
            personalized_recommendations = self._generate_goal_specific_recommendations(
                user_goals, goal_specific_analyses, expenses
            )
            
            # Kişiselleştirilmiş analiz promptu - ENHANCED
            prompt = f"""
            {user.first_name or user.username} kullanıcısının KAPSAMLI kişisel finansal analizi:

            🎯 HEDEF ANALİZİ:
            - Toplam hedef sayısı: {goal_analysis['total_goals']}
            - Toplam hedef tutarı: ₺{goal_analysis['total_target_amount']:,.2f}
            - Ortalama hedef büyüklüğü: ₺{goal_analysis['avg_goal_size']:,.2f}
            - Yüksek öncelikli hedefler: {goal_analysis['high_priority_count']}
            - En büyük hedef: {goal_analysis['largest_goal']['name']} (₺{goal_analysis['largest_goal']['amount']:,.2f})
            - Kategoriler: {', '.join(goal_analysis['categories'])}
            - Toplam ilerleme: %{goal_analysis['total_progress']:.1f}

            💸 HARCAMA ANALİZİ (Son 6 ay):
            - Toplam harcama: ₺{expense_analysis['total_expense']:,.2f}
            - Aylık ortalama: ₺{expense_analysis['monthly_average']:,.2f}
            - Günlük ortalama: ₺{expense_analysis['daily_average']:,.2f}
            - En çok harcanan kategori: {expense_analysis['top_category']} (₺{expense_analysis['top_amount']:,.2f})
            - Harcama çeşitliliği: {expense_analysis['category_count']} kategori
            - Büyük harcamalar (>₺500): {expense_analysis['big_expenses_count']} adet

            🔗 UYUMLULUK ANALİZİ:
            - Hedef-harcama uyumu: {compatibility_analysis['compatibility_score']}/10
            - Tasarruf potansiyeli: ₺{compatibility_analysis['saving_potential']:,.2f}/ay
            - Riskli harcama kategorileri: {', '.join(compatibility_analysis['risky_categories'])}
            - Hedef gerçekleşme süresi: {compatibility_analysis['realistic_timeline']}

            🎯 HEDEF-SPESİFİK ANALİZLER:
            {self._format_goal_specific_analyses_for_prompt(goal_specific_analyses)}

            💡 KİŞİSELLEŞTİRİLMİŞ ÖNERİLER:
            {personalized_recommendations}

            Bu VERİLERE VE HEDEF-SPESİFİK ANALİZLERE DAYANARAK, lütfen şu konularda DETAYLI ve ULTRA KİŞİSELLEŞTİRİLMİŞ analiz yap:

            1. HER HEDEFLE İLGİLİ SPESİFİK STRATEJİ DEĞERLENDİRMESİ
            2. HEDEFLERİN BİRBİRİYLE OLAN ETKİLEŞİMİ
            3. ÖNCELIKLEME VE ZAMAN YÖNETİMİ
            4. GERÇEK HEDEFLERİNE YÖNELIK SOMUT ADIMLAR
            5. RİSK YÖNETİMİ VE ALTERNATIF PLANLAR

            JSON formatında Türkçe cevap ver:
            {{
                "kisisel_durum": {{
                    "finansal_saglik_skoru": 85,
                    "hedef_stratejisi": "dengeli|agresif|muhafazakar",
                    "tasarruf_kapasitesi": "yüksek|orta|düşük",
                    "risk_profili": "düşük|orta|yüksek",
                    "genel_degerlendirme": "detaylı açıklama kişinin gerçek hedeflerini referans alarak"
                }},
                "hedef_analizi": {{
                    "en_onemli_hedef": "hedef adı",
                    "ilk_odaklanilmasi_gereken": "gerçek hedef adı",
                    "hedef_siralama_onerisi": ["gerçek hedef1", "gerçek hedef2", "gerçek hedef3"],
                    "hedef_etkilesimi": "hedeflerin birbirini nasıl etkilediği",
                    "gecersiz_timeline": "gerçek hedefler için timeline"
                }},
                "harcama_optimizasyonu": {{
                    "kesinti_yapilabilir_kategoriler": [
                        {{"kategori": "gerçek kategori", "mevcut": 600, "hedef": 400, "tasarruf": 200, "hedef_etkisi": "hangi hedefe yarayacak"}}
                    ],
                    "aylık_tasarruf_potansiyeli": 800,
                    "kritik_harcamalar": ["gerçek kategori adları"],
                    "hedef_spesifik_tasarruf": "her hedef için ayrı tasarruf stratejisi"
                }},
                "eylem_plani": [
                    {{
                        "ay": 1,
                        "hedefler": ["gerçek hedef1 için ₺X", "gerçek hedef2 için ₺Y"],
                        "harcama_hedefleri": {{"gerçek_kategori": "yeni_limit"}},
                        "odak": "spesifik ana görev",
                        "hedef_spesifik_adimlar": ["adım1", "adım2"]
                    }}
                ],
                "motivasyon_onerileri": [
                    "gerçek hedeflere yönelik kişiselleştirilmiş motivasyon 1",
                    "gerçek hedeflere yönelik kişiselleştirilmiş motivasyon 2"
                ],
                "risk_uyarilari": [
                    "gerçek hedefler için potansiyel risk 1",
                    "gerçek hedefler için potansiyel risk 2"
                ],
                "hedef_spesifik_stratejiler": {{
                    "acil_durum_fonu": "acil durum fonu varsa spesifik strateji",
                    "ev_pesınati": "ev peşinatı varsa spesifik strateji",
                    "tatil_fonu": "tatil fonu varsa spesifik strateji"
                }}
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen uzman bir kişisel finans danışmanısın. Kullanıcının GERÇEK verilerine ve SPESİFİK hedeflerine dayanarak, her hedef için ayrı ayrı özelleştirilmiş, uygulanabilir ve motivasyon verici finansal stratejiler geliştiriyorsun. Türkçe konuşuyorsun ve her tavsiyeni gerçek verilerle ve hedef türlerine göre özelleştiriyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,  # Daha uzun response için
                temperature=0.6
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'analysis': analysis,
                'goal_specific_data': goal_specific_analyses,  # YENİ: Hedef-spesifik analizler
                'data_summary': {
                    'goals': goal_analysis,
                    'expenses': expense_analysis,
                    'compatibility': compatibility_analysis
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_user_expenses(self, expenses):
        """Kullanıcının harcama verilerini analiz et"""
        if not expenses.exists():
            return {
                'total_expense': 0,
                'monthly_average': 0,
                'top_category': 'Veri yok',
                'trend': 'Veri yok'
            }
        
        total = sum(expense.amount for expense in expenses)
        monthly_avg = total / 6  # Son 6 ay
        
        # En çok harcanan kategori
        categories = {}
        for expense in expenses:
            cat = expense.category
            categories[cat] = categories.get(cat, 0) + expense.amount
        
        top_category = max(categories.items(), key=lambda x: x[1])[0] if categories else 'Belirtilmemiş'
        
        # Basit trend analizi (son 3 ay vs önceki 3 ay)
        now = timezone.now()
        three_months_ago = now - timedelta(days=90)
        
        recent_total = sum(e.amount for e in expenses if e.date >= three_months_ago)
        older_total = sum(e.amount for e in expenses if e.date < three_months_ago)
        
        if older_total == 0:
            trend = 'Yeni kullanıcı'
        elif recent_total > older_total:
            trend = 'Artış trendi'
        elif recent_total < older_total:
            trend = 'Azalış trendi'
        else:
            trend = 'Sabit'
        
        return {
            'total_expense': float(total),
            'monthly_average': float(monthly_avg),
            'top_category': top_category,
            'trend': trend
        }
    
    def _analyze_user_expenses_detailed(self, expenses):
        """Kullanıcının harcama verilerini detaylı analiz et"""
        if not expenses.exists():
            return {
                'total_expense': 0,
                'monthly_average': 0,
                'daily_average': 0,
                'top_category': 'Veri yok',
                'top_amount': 0,
                'category_count': 0,
                'big_expenses_count': 0,
                'trend': 'Veri yok'
            }
        
        total = sum(float(expense.amount) for expense in expenses)
        monthly_avg = total / 6  # Son 6 ay
        daily_avg = total / 180  # Son 180 gün
        
        # Kategori analizi
        categories = {}
        for expense in expenses:
            cat = expense.category.name
            categories[cat] = categories.get(cat, 0) + float(expense.amount)
        
        top_category = max(categories.items(), key=lambda x: x[1]) if categories else ('Belirtilmemiş', 0)
        
        # Büyük harcamalar (>500₺)
        big_expenses = [e for e in expenses if float(e.amount) > 500]
        
        return {
            'total_expense': total,
            'monthly_average': monthly_avg,
            'daily_average': daily_avg,
            'top_category': top_category[0],
            'top_amount': top_category[1],
            'category_count': len(categories),
            'big_expenses_count': len(big_expenses),
            'trend': self._calculate_expense_trend(expenses)
        }
    
    def _analyze_user_goals_detailed(self, goals):
        """Kullanıcının hedeflerini detaylı analiz et"""
        if not goals.exists():
            return {
                'total_goals': 0,
                'total_target_amount': 0,
                'avg_goal_size': 0,
                'high_priority_count': 0,
                'largest_goal': {'name': 'Yok', 'amount': 0},
                'categories': [],
                'total_progress': 0
            }
        
        goals_list = list(goals)
        total_target = sum(float(goal.target_amount) for goal in goals_list)
        avg_goal_size = total_target / len(goals_list)
        high_priority = [g for g in goals_list if g.priority == 1]
        largest_goal = max(goals_list, key=lambda g: g.target_amount)
        categories = list(set(goal.category for goal in goals_list))
        total_progress = sum(goal.progress_percentage for goal in goals_list) / len(goals_list)
        
        return {
            'total_goals': len(goals_list),
            'total_target_amount': total_target,
            'avg_goal_size': avg_goal_size,
            'high_priority_count': len(high_priority),
            'largest_goal': {'name': largest_goal.name, 'amount': float(largest_goal.target_amount)},
            'categories': categories,
            'total_progress': total_progress
        }
    
    def _analyze_goal_expense_compatibility(self, goals, expenses):
        """Hedefler ve harcamalar arasındaki uyumluluğu analiz et"""
        if not goals.exists() or not expenses.exists():
            return {
                'compatibility_score': 5,
                'saving_potential': 0,
                'risky_categories': [],
                'realistic_timeline': 'Belirlenemedi'
            }
        
        monthly_expense = sum(float(e.amount) for e in expenses) / 6
        total_target = sum(float(g.target_amount) for g in goals)
        monthly_goal_need = total_target / 24  # 2 yıl hedef
        
        # Uyumluluk skoru (0-10)
        if monthly_expense < monthly_goal_need:
            compatibility_score = 9  # Çok iyi
        elif monthly_expense < monthly_goal_need * 1.5:
            compatibility_score = 7  # İyi
        elif monthly_expense < monthly_goal_need * 2:
            compatibility_score = 5  # Orta
        else:
            compatibility_score = 3  # Düşük
        
        # Tasarruf potansiyeli
        saving_potential = max(0, monthly_expense * 0.2)  # %20 tasarruf potansiyeli
        
        # Riskli kategoriler (fazla harcanan)
        expense_categories = {}
        for expense in expenses:
            cat = expense.category.name
            expense_categories[cat] = expense_categories.get(cat, 0) + float(expense.amount)
        
        monthly_categories = {k: v/6 for k, v in expense_categories.items()}
        risky_categories = [cat for cat, amount in monthly_categories.items() 
                          if amount > 500 and cat in ['Eğlence', 'Giyim']]
        
        # Gerçekçi zaman çizelgesi
        if saving_potential > 0:
            months_needed = total_target / saving_potential
            if months_needed <= 12:
                realistic_timeline = f"{int(months_needed)} ay"
            elif months_needed <= 36:
                realistic_timeline = f"{int(months_needed/12)} yıl"
            else:
                realistic_timeline = "3+ yıl"
        else:
            realistic_timeline = "Mevcut durumda ulaşılamaz"
        
        return {
            'compatibility_score': compatibility_score,
            'saving_potential': saving_potential,
            'risky_categories': risky_categories,
            'realistic_timeline': realistic_timeline
        }
    
    def _calculate_expense_trend(self, expenses):
        """Harcama trendini hesapla"""
        if not expenses.exists():
            return 'Veri yok'
        
        # Son 3 ay vs önceki 3 ay karşılaştırması
        now = timezone.now()
        three_months_ago = now - timedelta(days=90)
        
        recent_expenses = [e for e in expenses if e.expense_date >= three_months_ago]
        older_expenses = [e for e in expenses if e.expense_date < three_months_ago]
        
        if not older_expenses:
            return 'Yetersiz veri'
        
        recent_total = sum(float(e.amount) for e in recent_expenses)
        older_total = sum(float(e.amount) for e in older_expenses)
        
        if recent_total > older_total * 1.1:
            return 'Artış trendi'
        elif recent_total < older_total * 0.9:
            return 'Azalış trendi'
        else:
            return 'Sabit trend'
