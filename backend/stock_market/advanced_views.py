"""
Finobai - Gelişmiş Borsa AI Views
Ultra modern borsa analizi ve yatırım önerileri API'leri
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any

from .models import (
    StockSymbol, StockPrice, StockAnalysis, UserPortfolio, 
    UserRiskProfile, PortfolioPosition, MarketNews
)
from .advanced_ai_service import AdvancedAIStockAnalyzer, PortfolioOptimizerService
from .services import StockDataService, MarketNewsService


@method_decorator(csrf_exempt, name='dispatch')
class UltraStockAnalysisView(APIView):
    """Ultra gelişmiş hisse analizi endpoint'i"""
    permission_classes = [AllowAny]  # Geçici - gerçek uygulamada IsAuthenticated
    
    def post(self, request):
        """Kapsamlı AI destekli hisse analizi"""
        try:
            symbol = request.data.get('symbol', '').strip().upper()
            include_user_profile = request.data.get('include_user_profile', False)
            
            if not symbol:
                return Response({
                    'success': False,
                    'error': 'Hisse sembolü gerekli (örn: THYAO.IS)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Kullanıcı profili varsa al
            user_profile = None
            if include_user_profile and request.user.is_authenticated:
                try:
                    user_profile = UserRiskProfile.objects.get(user=request.user)
                except UserRiskProfile.DoesNotExist:
                    pass
            
            # Gelişmiş AI analizi
            analyzer = AdvancedAIStockAnalyzer()
            comprehensive_analysis = analyzer.analyze_stock_comprehensive(symbol, user_profile)
            
            if comprehensive_analysis.get('error'):
                return Response({
                    'success': False,
                    'error': comprehensive_analysis['message']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Başarılı yanıt
            return Response({
                'success': True,
                'data': comprehensive_analysis,
                'generated_at': datetime.now().isoformat(),
                'analysis_type': 'comprehensive_ai_analysis',
                'user_personalized': user_profile is not None
            })
            
        except Exception as e:
            print(f"Ultra stock analysis error: {e}")
            return Response({
                'success': False,
                'error': 'Analiz yapılırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class AIPortfolioOptimizerView(APIView):
    """AI destekli portföy optimizasyonu"""
    permission_classes = [AllowAny]  # Geçici
    
    def post(self, request):
        """Kullanıcı profiline göre optimal portföy öner"""
        try:
            # Kullanıcı risk profili kontrolü
            if request.user.is_authenticated:
                try:
                    user_profile = UserRiskProfile.objects.get(user=request.user)
                except UserRiskProfile.DoesNotExist:
                    return Response({
                        'success': False,
                        'error': 'Önce risk profilinizi oluşturun'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Demo kullanım için varsayılan profil
                user_profile = self._create_demo_profile(request.data)
            
            # Analiz edilecek hisse listesi
            stock_symbols = request.data.get('stocks', [
                'THYAO.IS', 'AKBNK.IS', 'GARAN.IS', 'ASELS.IS', 
                'BIMAS.IS', 'TUPRS.IS', 'KCHOL.IS', 'ISCTR.IS'
            ])
            
            if not stock_symbols:
                return Response({
                    'success': False,
                    'error': 'Analiz edilecek hisse listesi gerekli'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Portföy optimizasyonu
            optimizer = PortfolioOptimizerService()
            optimized_portfolio = optimizer.optimize_portfolio(user_profile, stock_symbols)
            
            # Ek öneriler oluştur
            investment_recommendations = self._generate_investment_recommendations(
                optimized_portfolio, user_profile
            )
            
            # Risk uyarıları
            risk_warnings = self._generate_risk_warnings(optimized_portfolio, user_profile)
            
            # Başarılı yanıt
            return Response({
                'success': True,
                'data': {
                    'optimized_portfolio': optimized_portfolio,
                    'investment_recommendations': investment_recommendations,
                    'risk_warnings': risk_warnings,
                    'user_profile_summary': {
                        'risk_tolerance': user_profile.risk_tolerance if hasattr(user_profile, 'risk_tolerance') else 'MODERATE',
                        'investment_goal': user_profile.investment_goal if hasattr(user_profile, 'investment_goal') else 'BALANCED_GROWTH',
                        'monthly_budget': float(user_profile.monthly_investment_budget) if hasattr(user_profile, 'monthly_investment_budget') else 1000,
                        'investment_horizon': user_profile.investment_horizon if hasattr(user_profile, 'investment_horizon') else 12
                    },
                    'next_review_date': (datetime.now() + timedelta(days=90)).isoformat()[:10]
                },
                'generated_at': datetime.now().isoformat(),
                'analysis_type': 'portfolio_optimization'
            })
            
        except Exception as e:
            print(f"Portfolio optimization error: {e}")
            return Response({
                'success': False,
                'error': 'Portföy optimizasyonu yapılırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _create_demo_profile(self, data: Dict) -> Any:
        """Demo profil oluştur"""
        class DemoProfile:
            def __init__(self):
                self.risk_tolerance = data.get('risk_tolerance', 'MODERATE')
                self.investment_goal = data.get('investment_goal', 'BALANCED_GROWTH')
                self.monthly_investment_budget = data.get('monthly_budget', 1000)
                self.investment_horizon = data.get('investment_horizon', 12)
                self.experience_years = data.get('experience_years', 1)
        
        return DemoProfile()
    
    def _generate_investment_recommendations(self, portfolio: Dict, user_profile: Any) -> List[str]:
        """Yatırım önerileri oluştur"""
        recommendations = []
        
        # Portföy performansına göre öneriler
        expected_return = portfolio['portfolio_metrics']['expected_annual_return']
        
        if expected_return > 0.15:
            recommendations.append("🚀 Yüksek getiri potansiyeli - dikkatli pozisyon yönetimi yapın")
        elif expected_return < 0.05:
            recommendations.append("📈 Getiri potansiyelini artırmak için daha agresif hisseler düşünün")
        
        # Çeşitlendirme önerileri
        div_score = portfolio['diversification']['diversification_score']
        if div_score < 60:
            recommendations.append("🌐 Portföyünüzü daha fazla çeşitlendirin")
            recommendations.extend(portfolio['diversification']['recommendations'])
        
        # Risk toleransına göre öneriler
        risk_tolerance = getattr(user_profile, 'risk_tolerance', 'MODERATE')
        if risk_tolerance == 'CONSERVATIVE':
            recommendations.append("🛡️ Muhafazakar profilinize uygun güvenli varlıkları tercih edin")
            recommendations.append("💰 Portföyünüzün %20'sini nakit/tahvilde tutmayı düşünün")
        elif risk_tolerance == 'AGGRESSIVE':
            recommendations.append("⚡ Agresif profilinize uygun büyüme hisselerini değerlendirin")
            recommendations.append("🎯 Teknoloji ve gelişmekte olan sektörlere odaklanın")
        
        # Yatırım vadesi önerileri
        horizon = getattr(user_profile, 'investment_horizon', 12)
        if horizon < 12:
            recommendations.append("⏰ Kısa vadeli yatırım için likiditeye dikkat edin")
        elif horizon > 60:
            recommendations.append("🎯 Uzun vade avantajınızı kullanarak büyüme hisselerine odaklanın")
        
        return recommendations[:6]  # En fazla 6 öneri
    
    def _generate_risk_warnings(self, portfolio: Dict, user_profile: Any) -> List[str]:
        """Risk uyarıları oluştur"""
        warnings = []
        
        # Yüksek risk uyarısı
        portfolio_risk = portfolio['portfolio_metrics']['portfolio_risk_score']
        if portfolio_risk > 75:
            warnings.append("⚠️ Yüksek riskli portföy - değer kaybetme potansiyeli yüksek")
        
        # Konsantrasyon riski
        concentration_risk = portfolio['diversification']['concentration_risk']
        if concentration_risk > 40:
            warnings.append("🎯 Tek sektöre fazla yoğunlaşma riski")
        
        # Volatilite uyarısı
        volatility = portfolio['portfolio_metrics']['estimated_volatility']
        if volatility > 0.35:
            warnings.append("📊 Yüksek volatilite - fiyat dalgalanmaları beklenebilir")
        
        # Kullanıcı deneyim uyarısı
        experience = getattr(user_profile, 'experience_years', 1)
        if experience < 2 and portfolio_risk > 60:
            warnings.append("🔰 Yatırım deneyiminiz göz önünde bulundurularak dikkatli olun")
        
        return warnings


@method_decorator(csrf_exempt, name='dispatch')
class MarketSentimentView(APIView):
    """Piyasa sentiment analizi"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Genel piyasa sentiment analizi"""
        try:
            # Mock sentiment data - gerçek uygulamada gerçek veriler çekilecek
            market_sentiment = {
                'overall_sentiment': {
                    'score': 0.65,  # -1 ile 1 arası
                    'status': 'POZITIF',
                    'confidence': 78.5,
                    'description': 'Piyasa genel olarak iyimser, ancak dikkatli yaklaşım öneriliyor'
                },
                'fear_greed_index': {
                    'value': 72,
                    'status': 'AÇGÖZLÜLÜK',
                    'description': 'Yatırımcılar aşırı iyimser olabilir'
                },
                'volatility_index': {
                    'value': 28.5,
                    'status': 'ORTA',
                    'description': 'Normal seviyede volatilite'
                },
                'news_sentiment': {
                    'positive_news_ratio': 0.68,
                    'negative_news_ratio': 0.18,
                    'neutral_news_ratio': 0.14,
                    'trending_topics': [
                        'Merkez Bankası politikaları',
                        'Teknoloji hisselerinde yükseliş',
                        'Enerji sektörü gelişmeleri'
                    ]
                },
                'sector_sentiment': {
                    'Teknoloji': {'score': 0.8, 'trend': 'YÜKSELEN'},
                    'Bankacılık': {'score': 0.3, 'trend': 'DÜŞEN'},
                    'Enerji': {'score': 0.6, 'trend': 'YÜKSELEN'},
                    'Perakende': {'score': 0.4, 'trend': 'STABIL'},
                    'Ulaştırma': {'score': 0.5, 'trend': 'STABIL'}
                },
                'market_indicators': {
                    'bist_100_momentum': 'POZITIF',
                    'usd_try_trend': 'DÜŞÜŞ',
                    'interest_rate_expectation': 'STABIL',
                    'global_markets_correlation': 0.72
                },
                'ai_predictions': {
                    'next_week_outlook': 'IYIMSER',
                    'next_month_outlook': 'TEMKINLI_IYIMSER',
                    'key_risks': [
                        'Global piyasa volatilitesi',
                        'Jeopolitik gelişmeler',
                        'Para politikası değişiklikleri'
                    ],
                    'opportunities': [
                        'Teknoloji sektöründe değerlenme fırsatları',
                        'Enerji hisselerinde momentum',
                        'Temettü getirisi yüksek bankalar'
                    ]
                }
            }
            
            return Response({
                'success': True,
                'data': market_sentiment,
                'timestamp': datetime.now().isoformat(),
                'update_frequency': '15 dakikada bir',
                'data_sources': ['Reuters', 'Bloomberg', 'Finnet', 'Social Media APIs']
            })
            
        except Exception as e:
            print(f"Market sentiment error: {e}")
            return Response({
                'success': False,
                'error': 'Piyasa sentiment analizi yapılırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class PersonalizedStockScreenerView(APIView):
    """Kişiselleştirilmiş hisse tarayıcısı"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Kullanıcı kriterlerine göre hisse öner"""
        try:
            # Filtreleme kriterleri
            criteria = {
                'min_market_cap': request.data.get('min_market_cap', 0),
                'max_pe_ratio': request.data.get('max_pe_ratio', 50),
                'min_dividend_yield': request.data.get('min_dividend_yield', 0),
                'sectors': request.data.get('sectors', []),
                'risk_level': request.data.get('risk_level', 'ORTA'),
                'investment_style': request.data.get('investment_style', 'BALANCED'),
                'min_volume': request.data.get('min_volume', 1000000)
            }
            
            # Kullanıcı profili
            user_budget = request.data.get('budget', 10000)
            investment_horizon = request.data.get('investment_horizon', 12)
            
            # Mock hisse tarama sonuçları
            screened_stocks = self._perform_stock_screening(criteria, user_budget, investment_horizon)
            
            # AI öneriler
            ai_insights = self._generate_screening_insights(criteria, screened_stocks)
            
            return Response({
                'success': True,
                'data': {
                    'screened_stocks': screened_stocks,
                    'ai_insights': ai_insights,
                    'applied_criteria': criteria,
                    'total_matches': len(screened_stocks),
                    'screening_time': datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            print(f"Stock screening error: {e}")
            return Response({
                'success': False,
                'error': 'Hisse tarama işlemi başarısız'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _perform_stock_screening(self, criteria: Dict, budget: float, horizon: int) -> List[Dict]:
        """Hisse tarama işlemi"""
        # Mock tarama sonuçları - gerçek uygulamada veritabanı sorgusu yapılacak
        mock_results = [
            {
                'symbol': 'THYAO.IS',
                'name': 'Türk Hava Yolları',
                'sector': 'Ulaştırma',
                'current_price': 245.50,
                'market_cap': 3380000000,
                'pe_ratio': 12.5,
                'dividend_yield': 2.1,
                'volume': 2150000,
                'risk_score': 68,
                'ai_score': 85,
                'match_reasons': [
                    'P/E oranı kriterlere uygun',
                    'Yüksek işlem hacmi',
                    'Sektör tercihinizle uyumlu'
                ],
                'price_target': 285.00,
                'investment_thesis': 'Turizm toparlanması ile güçlü büyüme potansiyeli'
            },
            {
                'symbol': 'ASELS.IS',
                'name': 'Aselsan',
                'sector': 'Teknoloji',
                'current_price': 89.75,
                'market_cap': 196450000000,
                'pe_ratio': 15.8,
                'dividend_yield': 1.8,
                'volume': 3250000,
                'risk_score': 75,
                'ai_score': 92,
                'match_reasons': [
                    'Teknoloji sektörü lideri',
                    'Güçlü büyüme potansiyeli',
                    'Yüksek AI skoru'
                ],
                'price_target': 115.00,
                'investment_thesis': 'Savunma teknolojilerinde global oyuncu'
            },
            {
                'symbol': 'BIMAS.IS',
                'name': 'BİM',
                'sector': 'Perakende',
                'current_price': 485.00,
                'market_cap': 329550000000,
                'pe_ratio': 18.2,
                'dividend_yield': 3.2,
                'volume': 1850000,
                'risk_score': 45,
                'ai_score': 78,
                'match_reasons': [
                    'Düşük risk profili',
                    'İstikrarlı temettü',
                    'Güçlü finansal yapı'
                ],
                'price_target': 520.00,
                'investment_thesis': 'Perakende sektöründe güvenilir büyüme'
            }
        ]
        
        # Kriterlere göre filtrele
        filtered_results = []
        for stock in mock_results:
            if self._meets_criteria(stock, criteria):
                # Bütçeye göre önerilen miktar hesapla
                max_investment = min(budget * 0.2, budget / len(mock_results))  # Maksimum %20 veya eşit dağılım
                suggested_quantity = int(max_investment / stock['current_price'])
                stock['suggested_quantity'] = suggested_quantity
                stock['suggested_investment'] = suggested_quantity * stock['current_price']
                
                filtered_results.append(stock)
        
        # AI skoruna göre sırala
        filtered_results.sort(key=lambda x: x['ai_score'], reverse=True)
        
        return filtered_results[:10]  # En iyi 10 hisse
    
    def _meets_criteria(self, stock: Dict, criteria: Dict) -> bool:
        """Hisse kriterleri karşılıyor mu kontrol et"""
        if stock['market_cap'] < criteria['min_market_cap']:
            return False
        if stock['pe_ratio'] > criteria['max_pe_ratio']:
            return False
        if stock['dividend_yield'] < criteria['min_dividend_yield']:
            return False
        if criteria['sectors'] and stock['sector'] not in criteria['sectors']:
            return False
        if stock['volume'] < criteria['min_volume']:
            return False
        
        # Risk seviyesi kontrolü
        risk_level = criteria['risk_level']
        if risk_level == 'DÜŞÜK' and stock['risk_score'] > 60:
            return False
        elif risk_level == 'YÜKSEK' and stock['risk_score'] < 60:
            return False
        
        return True
    
    def _generate_screening_insights(self, criteria: Dict, results: List[Dict]) -> Dict[str, Any]:
        """Tarama sonuçları için AI öngörüleri"""
        if not results:
            return {
                'summary': 'Kriterlere uygun hisse bulunamadı',
                'suggestions': ['Kriterleri gevşetin', 'Farklı sektörlere bakın'],
                'market_opportunities': []
            }
        
        avg_ai_score = sum(stock['ai_score'] for stock in results) / len(results)
        avg_risk = sum(stock['risk_score'] for stock in results) / len(results)
        
        insights = {
            'summary': f"{len(results)} adet uygun hisse bulundu. Ortalama AI skoru: {avg_ai_score:.1f}",
            'portfolio_quality': 'YÜKSEK' if avg_ai_score > 80 else 'ORTA' if avg_ai_score > 70 else 'DÜŞÜK',
            'risk_assessment': 'YÜKSEK' if avg_risk > 70 else 'ORTA' if avg_risk > 50 else 'DÜŞÜK',
            'top_picks': [
                {
                    'symbol': results[0]['symbol'],
                    'reason': f"En yüksek AI skoru: {results[0]['ai_score']}"
                },
                {
                    'symbol': results[1]['symbol'] if len(results) > 1 else results[0]['symbol'],
                    'reason': 'İkinci en iyi seçenek'
                }
            ] if results else [],
            'diversification_advice': self._get_diversification_advice(results),
            'timing_insights': [
                'Teknoloji sektöründe değerlenme fırsatları var',
                'Enerji hisselerinde momentum devam ediyor',
                'Bankacılık sektöründe temkinli yaklaşım öneriliyor'
            ]
        }
        
        return insights
    
    def _get_diversification_advice(self, stocks: List[Dict]) -> List[str]:
        """Çeşitlendirme tavsiyeleri"""
        sectors = {}
        for stock in stocks:
            sector = stock['sector']
            sectors[sector] = sectors.get(sector, 0) + 1
        
        advice = []
        
        if len(sectors) < 3:
            advice.append("Daha fazla sektöre yayılım yapın")
        
        max_sector = max(sectors, key=sectors.get) if sectors else None
        if max_sector and sectors[max_sector] > len(stocks) * 0.5:
            advice.append(f"{max_sector} sektöründeki yoğunluğu azaltın")
        
        if not advice:
            advice.append("Sektör dağılımı dengeli görünüyor")
        
        return advice


@method_decorator(csrf_exempt, name='dispatch')
class RealTimeStockAlertsView(APIView):
    """Gerçek zamanlı hisse uyarıları"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Aktif uyarıları getir"""
        try:
            # Mock uyarılar - gerçek uygulamada Redis/WebSocket kullanılacak
            alerts = [
                {
                    'id': 1,
                    'type': 'PRICE_ALERT',
                    'symbol': 'THYAO.IS',
                    'message': 'THY hedef fiyata ulaştı: 245.50₺',
                    'severity': 'INFO',
                    'timestamp': datetime.now().isoformat(),
                    'action_required': False
                },
                {
                    'id': 2,
                    'type': 'TECHNICAL_ALERT',
                    'symbol': 'ASELS.IS',
                    'message': 'ASELSAN RSI 70 üzerine çıktı - Aşırı alım bölgesi',
                    'severity': 'WARNING',
                    'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(),
                    'action_required': True,
                    'suggested_action': 'Kâr realizasyonu düşünün'
                },
                {
                    'id': 3,
                    'type': 'NEWS_ALERT',
                    'symbol': 'GARAN.IS',
                    'message': 'Garanti Bankası üç aylık sonuçları beklentileri aştı',
                    'severity': 'POSITIVE',
                    'timestamp': (datetime.now() - timedelta(minutes=15)).isoformat(),
                    'action_required': False
                },
                {
                    'id': 4,
                    'type': 'PORTFOLIO_ALERT',
                    'symbol': 'PORTFOLIO',
                    'message': 'Portföy değeriniz %5 yükseldi - Kâr realizasyonu düşünün',
                    'severity': 'SUCCESS',
                    'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
                    'action_required': False
                }
            ]
            
            # Kullanıcı ayarları (mock)
            user_settings = {
                'price_alerts_enabled': True,
                'technical_alerts_enabled': True,
                'news_alerts_enabled': True,
                'portfolio_alerts_enabled': True,
                'notification_frequency': 'REAL_TIME'
            }
            
            return Response({
                'success': True,
                'data': {
                    'active_alerts': alerts,
                    'user_settings': user_settings,
                    'alert_count': len(alerts),
                    'unread_count': len([a for a in alerts if a['action_required']]),
                    'last_update': datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            print(f"Alerts error: {e}")
            return Response({
                'success': False,
                'error': 'Uyarılar alınırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Yeni uyarı oluştur"""
        try:
            alert_data = {
                'symbol': request.data.get('symbol'),
                'alert_type': request.data.get('alert_type'),  # PRICE_ABOVE, PRICE_BELOW, RSI_OVERBOUGHT, etc.
                'threshold_value': request.data.get('threshold_value'),
                'notification_method': request.data.get('notification_method', 'IN_APP')
            }
            
            # Uyarı doğrulaması
            if not all([alert_data['symbol'], alert_data['alert_type'], alert_data['threshold_value']]):
                return Response({
                    'success': False,
                    'error': 'Eksik uyarı bilgileri'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Mock uyarı oluşturma - gerçek uygulamada veritabanına kaydet
            new_alert = {
                'id': 99,
                'user_id': getattr(request.user, 'id', 'demo'),
                'symbol': alert_data['symbol'],
                'alert_type': alert_data['alert_type'],
                'threshold_value': alert_data['threshold_value'],
                'is_active': True,
                'created_at': datetime.now().isoformat(),
                'triggered_count': 0
            }
            
            return Response({
                'success': True,
                'data': {
                    'alert': new_alert,
                    'message': 'Uyarı başarıyla oluşturuldu'
                }
            })
            
        except Exception as e:
            print(f"Create alert error: {e}")
            return Response({
                'success': False,
                'error': 'Uyarı oluşturulurken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
