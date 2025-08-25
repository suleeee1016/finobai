"""
Hedef-spesifik analiz algoritmaları
Her hedef türü için özelleştirilmiş analiz stratejileri
"""
from typing import Dict, List, Any, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Avg, Count
import statistics


class GoalSpecificAnalyzer:
    """Hedef tipine göre özelleştirilmiş analiz algoritmaları"""
    
    def __init__(self):
        self.goal_type_strategies = {
            'emergency': self.analyze_emergency_fund,
            'house': self.analyze_house_goal,
            'vacation': self.analyze_vacation_goal,
            'car': self.analyze_car_goal,
            'wedding': self.analyze_wedding_goal,
            'education': self.analyze_education_goal,
            'retirement': self.analyze_retirement_goal,
            'health': self.analyze_health_goal,
            'investment': self.analyze_investment_goal,
            'custom': self.analyze_custom_goal
        }
    
    def analyze_goal_specifically(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Ana method: Hedefe göre spesifik analiz yap"""
        
        # Genel analiz metrikleri
        base_analysis = self._calculate_base_metrics(goal, expenses)
        
        # Hedef-spesifik analiz
        specific_analyzer = self.goal_type_strategies.get(
            goal.category, 
            self.analyze_custom_goal
        )
        specific_analysis = specific_analyzer(goal, expenses, user_profile)
        
        # Analiz sonuçlarını birleştir
        combined_analysis = {
            **base_analysis,
            **specific_analysis,
            'goal_category': goal.category,
            'analysis_timestamp': timezone.now().isoformat(),
        }
        
        return combined_analysis
    
    def _calculate_base_metrics(self, goal, expenses) -> Dict[str, Any]:
        """Tüm hedefler için temel metrikler"""
        current_progress = float(goal.progress_percentage)
        monthly_target = float(goal.target_amount) / max(goal.months_remaining, 1)
        
        return {
            'goal_name': goal.name,
            'target_amount': float(goal.target_amount),
            'current_amount': float(goal.current_amount),
            'progress_percentage': current_progress,
            'months_remaining': goal.months_remaining,
            'monthly_target_needed': monthly_target,
            'monthly_contribution_planned': float(goal.monthly_contribution),
            'feasibility_score': self._calculate_feasibility_score(goal, expenses),
        }
    
    def _calculate_feasibility_score(self, goal, expenses) -> float:
        """Hedefe ulaşabilirlik skoru (0-100)"""
        # Çeşitli faktörleri göz önünde bulundur
        time_factor = max(0, min(100, goal.months_remaining * 2))  # Zaman faktörü
        progress_factor = float(goal.progress_percentage)  # Mevcut ilerleme
        
        # Harcama analizi
        monthly_expense = sum(float(e.amount) for e in expenses) / 6
        income_estimate = monthly_expense * 1.3  # Harcamanın %130'u gelir tahmini
        
        savings_capacity = max(0, income_estimate - monthly_expense)
        required_savings = float(goal.target_amount) / max(goal.months_remaining, 1)
        
        savings_factor = min(100, (savings_capacity / max(required_savings, 1)) * 100) if required_savings > 0 else 100
        
        # Ağırlıklı ortalama
        feasibility = (time_factor * 0.3 + progress_factor * 0.3 + savings_factor * 0.4)
        return round(feasibility, 1)

    # =============================================================================
    # HEDEFLERİN SPESİFİK ANALİZ ALGORİTMALARI
    # =============================================================================

    def analyze_emergency_fund(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Acil Durum Fonu - Stabilite odaklı analiz"""
        
        # Aylık harcama ortalaması
        monthly_expenses = sum(float(e.amount) for e in expenses) / 6
        
        # Acil durum fonu için ideal tutar (6-12 aylık harcama)
        ideal_min = monthly_expenses * 6
        ideal_max = monthly_expenses * 12
        
        # Risk faktörleri - harcamalardaki ani artışlar
        expense_volatility = self._calculate_expense_volatility(expenses)
        
        # Kritik kategoriler (kesinti yapılabilir)
        non_essential_spending = self._identify_non_essential_spending(expenses)
        
        return {
            'strategy_type': 'stability_focused',
            'monthly_expense_average': round(monthly_expenses, 2),
            'ideal_range': {
                'minimum': round(ideal_min, 2),
                'maximum': round(ideal_max, 2)
            },
            'current_coverage_months': round(float(goal.current_amount) / monthly_expenses, 1) if monthly_expenses > 0 else 0,
            'expense_volatility_score': expense_volatility,
            'reducible_expenses': non_essential_spending,
            'priority_level': 'critical',
            'specific_recommendations': [
                f"Aylık harcamanız ₺{monthly_expenses:,.0f}, ideal fon ₺{ideal_min:,.0f}-₺{ideal_max:,.0f} arasında olmalı",
                "İlk hedef: 3 aylık harcama tutarı",
                "Eğlence ve giyim harcamalarını geçici olarak azaltmayı değerlendirin",
                "Düzenli otomatik transfer ayarlayın"
            ],
            'urgency_factors': self._calculate_emergency_urgency(user_profile, expenses)
        }

    def analyze_house_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Ev Almak - Uzun vadeli büyük hedef analizi"""
        
        # Peşinat oranı analizi (genelde %20-30)
        estimated_house_price = float(goal.target_amount) / 0.25  # %25 peşinat varsayımı
        
        # Konut kredisi uygunluğu (aylık gelirin %30'u kredi taksidi)
        monthly_expenses = sum(float(e.amount) for e in expenses) / 6
        estimated_income = monthly_expenses * 1.4
        max_monthly_payment = estimated_income * 0.3
        
        # Kira vs. kredi karşılaştırması
        current_rent = self._estimate_current_rent(expenses)
        
        # Market timing factors
        timeline_analysis = self._analyze_housing_market_timing(goal)
        
        return {
            'strategy_type': 'long_term_major',
            'estimated_house_price': round(estimated_house_price, 2),
            'down_payment_percentage': 25,
            'estimated_monthly_income': round(estimated_income, 2),
            'max_affordable_monthly_payment': round(max_monthly_payment, 2),
            'current_rent_estimate': round(current_rent, 2),
            'rent_vs_mortgage_analysis': {
                'current_annual_rent': round(current_rent * 12, 2),
                'potential_savings': round((current_rent - max_monthly_payment) * 12, 2) if current_rent > max_monthly_payment else 0
            },
            'timeline_analysis': timeline_analysis,
            'specific_recommendations': [
                f"₺{estimated_house_price:,.0f} değerindeki ev için ₺{goal.target_amount:,.0f} peşinat hedefliyorsunuz",
                f"Aylık kredi ödeme kapasitesi: ₺{max_monthly_payment:,.0f}",
                "Kredi başvurusu öncesi kredi puanınızı kontrol edin",
                "Emlak piyasası araştırması yapın",
                "Ev satın alma masraflarını (tapu, noter, emlak vergisi) de hesaba katın"
            ],
            'risk_factors': self._analyze_housing_risks(goal, expenses),
            'priority_level': 'high'
        }

    def analyze_vacation_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Tatil - Kısa vadeli motivasyon odaklı"""
        
        # Tatil türü ve budget analizi
        vacation_type = self._classify_vacation_budget(goal.target_amount)
        
        # Seasonal timing
        seasonal_recommendations = self._analyze_vacation_timing(goal)
        
        # Experience vs. luxury balance
        spending_philosophy = self._analyze_leisure_spending(expenses)
        
        return {
            'strategy_type': 'short_term_reward',
            'vacation_classification': vacation_type,
            'seasonal_timing': seasonal_recommendations,
            'spending_philosophy': spending_philosophy,
            'motivation_factors': {
                'deadline_urgency': 'medium',
                'reward_frequency': 'periodic',
                'psychological_impact': 'high'
            },
            'specific_recommendations': [
                f"₺{goal.target_amount:,.0f} bütçeli {vacation_type['type']} planı",
                "Erken rezervasyon indirimlerini değerlendirin",
                "Tatil dönemine 3-6 ay kala rezervasyon yapın",
                "Günlük harcama limitini önceden belirleyin"
            ],
            'budget_breakdown': vacation_type.get('budget_breakdown', {}),
            'priority_level': 'medium'
        }

    def analyze_car_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Araç Almak - Pratik ihtiyaç odaklı"""
        
        # Mevcut ulaşım maliyeti analizi
        current_transport_cost = self._calculate_transport_costs(expenses)
        
        # Yeni vs. ikinci el analizi
        car_options = self._analyze_car_options(goal.target_amount)
        
        # Toplam sahip olma maliyeti
        ownership_costs = self._calculate_car_ownership_costs(goal.target_amount)
        
        return {
            'strategy_type': 'practical_necessity',
            'current_transport_cost': round(current_transport_cost, 2),
            'car_options': car_options,
            'ownership_costs': ownership_costs,
            'cost_benefit_analysis': {
                'monthly_savings': round(current_transport_cost - ownership_costs['monthly_total'], 2),
                'break_even_months': round(float(goal.target_amount) / max(current_transport_cost - ownership_costs['monthly_total'], 1), 0) if current_transport_cost > ownership_costs['monthly_total'] else None
            },
            'specific_recommendations': [
                f"Mevcut ulaşım maliyetiniz: ₺{current_transport_cost:,.0f}/ay",
                f"Araç sahip olma toplam maliyeti: ₺{ownership_costs['monthly_total']:,.0f}/ay",
                "Kasko ve trafik sigortası fiyatlarını araştırın",
                "Yakıt tüketimi düşük modelleri değerlendirin"
            ],
            'priority_level': 'high'
        }

    def analyze_wedding_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Düğün - Sosyal ve duygusal değer odaklı"""
        
        # Guest count estimation based on budget
        estimated_guests = int(float(goal.target_amount) / 150)  # ₺150 per person estimate
        
        # Wedding category analysis
        wedding_tier = self._classify_wedding_budget(goal.target_amount)
        
        # Seasonal cost differences
        seasonal_costs = self._analyze_wedding_seasonality(goal)
        
        return {
            'strategy_type': 'social_milestone',
            'estimated_guest_count': estimated_guests,
            'wedding_tier': wedding_tier,
            'seasonal_cost_analysis': seasonal_costs,
            'budget_allocation': {
                'venue_catering': 0.5,  # %50
                'photography_music': 0.2,  # %20
                'dress_suit': 0.1,  # %10
                'flowers_decoration': 0.1,  # %10
                'misc_contingency': 0.1  # %10
            },
            'specific_recommendations': [
                f"₺{goal.target_amount:,.0f} bütçe ile yaklaşık {estimated_guests} kişilik düğün",
                "Sezon dışı tarihler %20-30 daha uygun olabilir",
                "Erken rezervasyon %15-20 tasarruf sağlayabilir",
                "Detaylı düğün bütçesi çizelgesi hazırlayın"
            ],
            'timeline_considerations': self._analyze_wedding_timeline(goal),
            'priority_level': 'high'
        }

    def analyze_education_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Eğitim - Yatırım geri dönüşü odaklı"""
        
        # ROI potential analysis
        roi_analysis = self._calculate_education_roi(goal.target_amount)
        
        # Education type classification
        education_type = self._classify_education_investment(goal.target_amount)
        
        # Alternative funding options
        funding_options = self._analyze_education_funding(goal)
        
        return {
            'strategy_type': 'investment_return',
            'roi_analysis': roi_analysis,
            'education_type': education_type,
            'funding_alternatives': funding_options,
            'investment_perspective': {
                'payback_period_years': roi_analysis.get('payback_years', 'unknown'),
                'lifetime_value_increase': roi_analysis.get('lifetime_value', 0),
                'career_impact_score': roi_analysis.get('career_impact', 'medium')
            },
            'specific_recommendations': [
                f"₺{goal.target_amount:,.0f} eğitim yatırımı",
                "Eğitim kredisi seçeneklerini araştırın",
                "Burs imkanlarını değerlendirin",
                "Part-time çalışma olanaklarını göz önünde bulundurun"
            ],
            'priority_level': 'high'
        }

    def analyze_retirement_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Emeklilik - Ultra uzun vadeli birikim"""
        
        # Compound interest projections
        retirement_projections = self._calculate_retirement_projections(goal, user_profile)
        
        # Inflation adjustment
        inflation_adjusted = self._calculate_inflation_impact(goal, retirement_projections)
        
        return {
            'strategy_type': 'ultra_long_term',
            'retirement_projections': retirement_projections,
            'inflation_considerations': inflation_adjusted,
            'specific_recommendations': [
                "Emeklilik için compound interest'ten maximum faydalanın",
                "Otomatik yatırım planı kurun",
                "Vergi avantajlı emeklilik hesaplarını değerlendirin"
            ],
            'priority_level': 'medium'
        }

    def analyze_health_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Sağlık - Kritik önem taşıyan hedef"""
        
        # Health emergency analysis
        health_priorities = self._analyze_health_priorities(goal, expenses)
        
        return {
            'strategy_type': 'health_critical',
            'health_priorities': health_priorities,
            'specific_recommendations': [
                "Sağlık harcamaları öncelikli olarak değerlendirilmelidir",
                "Sağlık sigortası seçeneklerini araştırın"
            ],
            'priority_level': 'critical'
        }

    def analyze_investment_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Yatırım - Büyüme odaklı"""
        
        # Risk tolerance analysis
        risk_analysis = self._analyze_investment_risk_tolerance(expenses, user_profile)
        
        return {
            'strategy_type': 'growth_focused',
            'risk_analysis': risk_analysis,
            'specific_recommendations': [
                "Yatırım portföyü çeşitlendirme",
                "Risk toleransınıza uygun enstrümanları seçin"
            ],
            'priority_level': 'medium'
        }

    def analyze_custom_goal(self, goal, expenses, user_profile) -> Dict[str, Any]:
        """Özel hedef - Genel analiz"""
        
        return {
            'strategy_type': 'custom_flexible',
            'specific_recommendations': [
                f"₺{goal.target_amount:,.0f} hedefli özel planınız",
                "Hedef detaylarını netleştirin",
                "Benzer hedeflerle karşılaştırma yapın"
            ],
            'priority_level': 'medium'
        }

    # =============================================================================
    # YARDIMCI ANALİZ METHODLARİ
    # =============================================================================

    def _calculate_expense_volatility(self, expenses) -> float:
        """Harcama dalgalanma skoru"""
        if len(expenses) < 3:
            return 0.5  # Neutral score
        
        amounts = [float(e.amount) for e in expenses]
        mean_amount = statistics.mean(amounts)
        volatility = statistics.stdev(amounts) / mean_amount if mean_amount > 0 else 0
        
        # 0-1 arası normalize et
        return min(1.0, volatility)

    def _identify_non_essential_spending(self, expenses) -> List[Dict]:
        """Kesinti yapılabilir harcama kategorileri"""
        categories = {}
        for expense in expenses:
            cat_name = expense.category.name
            categories[cat_name] = categories.get(cat_name, 0) + float(expense.amount)
        
        # Non-essential kategoriler
        non_essential = ['Eğlence', 'Giyim', 'Hobi', 'Kozmetik']
        reducible = []
        
        for cat_name, total in categories.items():
            if cat_name in non_essential and total > 500:  # Aylık 500₺ üzeri
                monthly_avg = total / 6
                potential_reduction = monthly_avg * 0.3  # %30 azaltma
                reducible.append({
                    'category': cat_name,
                    'current_monthly': round(monthly_avg, 2),
                    'potential_reduction': round(potential_reduction, 2),
                    'reduction_percentage': 30
                })
        
        return reducible

    def _classify_vacation_budget(self, target_amount: Decimal) -> Dict[str, Any]:
        """Tatil bütçesine göre kategori belirleme"""
        amount = float(target_amount)
        
        if amount <= 5000:
            return {
                'type': 'Yerel Tatil',
                'category': 'budget',
                'duration_days': '2-4',
                'budget_breakdown': {
                    'accommodation': 0.4,
                    'food': 0.3,
                    'activities': 0.2,
                    'transport': 0.1
                }
            }
        elif amount <= 15000:
            return {
                'type': 'Yurt İçi Tatil',
                'category': 'mid_range',
                'duration_days': '5-7',
                'budget_breakdown': {
                    'accommodation': 0.35,
                    'food': 0.25,
                    'activities': 0.25,
                    'transport': 0.15
                }
            }
        else:
            return {
                'type': 'Yurt Dışı Tatil',
                'category': 'premium',
                'duration_days': '7-14',
                'budget_breakdown': {
                    'accommodation': 0.3,
                    'food': 0.2,
                    'activities': 0.2,
                    'transport': 0.3
                }
            }

    def _calculate_transport_costs(self, expenses) -> float:
        """Mevcut ulaşım maliyetlerini hesapla"""
        transport_total = 0
        for expense in expenses:
            if expense.category.name in ['Ulaşım', 'Yakıt', 'Toplu Taşıma']:
                transport_total += float(expense.amount)
        
        return transport_total / 6  # Aylık ortalama

    def _calculate_car_ownership_costs(self, target_amount: Decimal) -> Dict[str, float]:
        """Araç sahip olma toplam maliyeti"""
        car_value = float(target_amount)
        
        # Tahmini aylık maliyetler
        insurance = car_value * 0.02 / 12  # Yıllık %2 sigorta
        maintenance = 300  # Aylık bakım
        fuel = 800  # Aylık yakıt tahmini
        depreciation = car_value * 0.15 / 12  # Yıllık %15 değer kaybı
        
        return {
            'insurance': round(insurance, 2),
            'maintenance': maintenance,
            'fuel': fuel,
            'depreciation': round(depreciation, 2),
            'monthly_total': round(insurance + maintenance + fuel + depreciation, 2)
        }

    def _analyze_car_options(self, target_amount: Decimal) -> Dict[str, Any]:
        """Araç seçenekleri analizi"""
        amount = float(target_amount)
        
        if amount <= 100000:
            return {
                'category': 'Ekonomik Araç',
                'type': 'used_car',
                'age_range': '3-7 yaş',
                'fuel_efficiency': 'high',
                'maintenance_cost': 'low'
            }
        elif amount <= 300000:
            return {
                'category': 'Orta Segment',
                'type': 'new_or_recent',
                'age_range': '0-3 yaş',
                'fuel_efficiency': 'medium',
                'maintenance_cost': 'medium'
            }
        else:
            return {
                'category': 'Premium Araç',
                'type': 'luxury_new',
                'age_range': '0-1 yaş',
                'fuel_efficiency': 'variable',
                'maintenance_cost': 'high'
            }

    def _classify_wedding_budget(self, target_amount: Decimal) -> Dict[str, Any]:
        """Düğün bütçesi kategorisi"""
        amount = float(target_amount)
        
        if amount <= 50000:
            return {
                'tier': 'İntim Düğün',
                'guest_capacity': '20-50',
                'venue_type': 'restaurant_small_hall'
            }
        elif amount <= 150000:
            return {
                'tier': 'Orta Ölçek Düğün',
                'guest_capacity': '50-150',
                'venue_type': 'wedding_hall'
            }
        else:
            return {
                'tier': 'Büyük Düğün',
                'guest_capacity': '150+',
                'venue_type': 'luxury_venue'
            }

    def _calculate_education_roi(self, target_amount: Decimal) -> Dict[str, Any]:
        """Eğitim yatırımının geri dönüşü"""
        amount = float(target_amount)
        
        # Basit ROI hesaplama
        if amount <= 20000:
            income_increase = amount * 0.3  # %30 gelir artışı
            payback_years = 3
        elif amount <= 100000:
            income_increase = amount * 0.4  # %40 gelir artışı  
            payback_years = 4
        else:
            income_increase = amount * 0.5  # %50 gelir artışı
            payback_years = 5
        
        return {
            'annual_income_increase': round(income_increase / payback_years, 2),
            'payback_years': payback_years,
            'lifetime_value': round(income_increase * 10, 2),  # 10 yıllık değer
            'career_impact': 'high' if amount > 50000 else 'medium'
        }

    def _classify_education_investment(self, target_amount: Decimal) -> Dict[str, Any]:
        """Eğitim türü sınıflandırması"""
        amount = float(target_amount)
        
        if amount <= 30000:
            return {
                'type': 'Kurs/Sertifika',
                'duration': '3-12 ay',
                'impact': 'skill_upgrade'
            }
        elif amount <= 100000:
            return {
                'type': 'Lisans Tamamlama/MBA',
                'duration': '1-2 yıl',
                'impact': 'career_advancement'
            }
        else:
            return {
                'type': 'Yurt Dışı Eğitim',
                'duration': '2-4 yıl',
                'impact': 'major_career_shift'
            }

    # Diğer yardımcı methodlar için placeholder'lar
    def _calculate_emergency_urgency(self, user_profile, expenses):
        return {'urgency_score': 0.8, 'factors': ['irregular_income', 'high_debt']}
    
    def _estimate_current_rent(self, expenses):
        return 2000  # Placeholder
    
    def _analyze_housing_market_timing(self, goal):
        return {'market_condition': 'stable', 'timing_recommendation': 'good_time_to_buy'}
    
    def _analyze_housing_risks(self, goal, expenses):
        return ['interest_rate_risk', 'market_volatility']
    
    def _analyze_vacation_timing(self, goal):
        return {'best_months': ['May', 'September'], 'avoid_months': ['July', 'August']}
    
    def _analyze_leisure_spending(self, expenses):
        return {'philosophy': 'experience_focused', 'budget_allocation': 'balanced'}
    
    def _analyze_wedding_seasonality(self, goal):
        return {'peak_season': 'May-September', 'off_season_savings': 25}
    
    def _analyze_wedding_timeline(self, goal):
        return {'planning_months_needed': 12, 'booking_deadlines': 'venue_6_months'}
    
    def _analyze_education_funding(self, goal):
        return ['scholarship', 'education_loan', 'employer_sponsorship']
    
    def _calculate_retirement_projections(self, goal, user_profile):
        return {'projected_value': float(goal.target_amount) * 2, 'compound_rate': 0.07}
    
    def _calculate_inflation_impact(self, goal, projections):
        return {'real_value': projections['projected_value'] * 0.7, 'inflation_rate': 0.05}
    
    def _analyze_health_priorities(self, goal, expenses):
        return {'category': 'preventive_care', 'urgency': 'medium'}
    
    def _analyze_investment_risk_tolerance(self, expenses, user_profile):
        return {'risk_level': 'moderate', 'recommended_allocation': {'stocks': 0.6, 'bonds': 0.4}}
