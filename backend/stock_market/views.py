from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
import json

from .models import StockSymbol, StockPrice, StockAnalysis, UserPortfolio, UserRiskProfile
from .services import StockDataService, StockAnalysisService, MarketNewsService


@method_decorator(csrf_exempt, name='dispatch')
class StockPricesView(APIView):
    """Hisse senedi fiyatları endpoint'i"""
    permission_classes = [AllowAny]  # Geçici
    
    def get(self, request):
        """Güncel hisse fiyatlarını getir"""
        try:
            # Mock BIST hisse verileri
            mock_stocks = [
                {
                    'symbol': 'THYAO.IS',
                    'name': 'Türk Hava Yolları',
                    'current_price': 245.50,
                    'change_percent': 3.25,
                    'change_amount': 7.75,
                    'volume': 2150000,
                    'market_cap': 3380000000,
                    'sector': 'Havayolu',
                    'currency': 'TRY'
                },
                {
                    'symbol': 'AKBNK.IS',
                    'name': 'Akbank',
                    'current_price': 58.20,
                    'change_percent': -1.85,
                    'change_amount': -1.10,
                    'volume': 15400000,
                    'market_cap': 302890000000,
                    'sector': 'Bankacılık',
                    'currency': 'TRY'
                },
                {
                    'symbol': 'ASELS.IS',
                    'name': 'Aselsan',
                    'current_price': 89.75,
                    'change_percent': 5.15,
                    'change_amount': 4.40,
                    'volume': 3250000,
                    'market_cap': 196450000000,
                    'sector': 'Savunma',
                    'currency': 'TRY'
                },
                {
                    'symbol': 'GARAN.IS',
                    'name': 'Garanti BBVA',
                    'current_price': 95.80,
                    'change_percent': 2.10,
                    'change_amount': 1.97,
                    'volume': 8750000,
                    'market_cap': 402360000000,
                    'sector': 'Bankacılık',
                    'currency': 'TRY'
                },
                {
                    'symbol': 'BIMAS.IS',
                    'name': 'BİM',
                    'current_price': 485.00,
                    'change_percent': -0.65,
                    'change_amount': -3.17,
                    'volume': 1850000,
                    'market_cap': 329550000000,
                    'sector': 'Perakende',
                    'currency': 'TRY'
                },
                {
                    'symbol': 'TUPRS.IS',
                    'name': 'Tüpraş',
                    'current_price': 128.40,
                    'change_percent': 4.35,
                    'change_amount': 5.35,
                    'volume': 2950000,
                    'market_cap': 278550000000,
                    'sector': 'Enerji',
                    'currency': 'TRY'
                }
            ]
            
            return Response({
                'stocks': mock_stocks,
                'timestamp': datetime.now().isoformat(),
                'market_status': 'OPEN',  # OPEN, CLOSED, PRE_MARKET
                'total_count': len(mock_stocks)
            })
            
        except Exception as e:
            print(f"Stock prices error: {e}")
            return Response({
                'error': 'Hisse fiyatları alınırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StockAnalysisView(APIView):
    """Hisse analizi endpoint'i"""
    permission_classes = [AllowAny]  # Geçici
    
    def post(self, request):
        """Belirli bir hisse için AI analizi yap"""
        try:
            symbol = request.data.get('symbol', '').strip().upper()
            
            if not symbol:
                return Response({
                    'error': 'Hisse sembolü gerekli (örn: THYAO.IS)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Mock hisse analizi
            mock_analyses = {
                'THYAO.IS': {
                    'symbol': 'THYAO.IS',
                    'name': 'Türk Hava Yolları',
                    'current_price': 245.50,
                    'recommendation': 'BUY',
                    'recommendation_text': 'Al',
                    'risk_level': 'MEDIUM',
                    'risk_text': 'Orta Risk',
                    'confidence_score': 78.5,
                    'target_price': 285.00,
                    'stop_loss_price': 210.00,
                    'analysis_text': 'THY, turizm sektöründeki toparlanma ile birlikte güçlü bir performans sergiliyor. Uluslararası uçuş ağının genişlemesi ve operasyonel verimlilikteki iyileşmeler olumlu. Ancak yakıt fiyatlarındaki volatilite risk faktörü.',
                    'key_factors': [
                        'Turizm sektöründe toparlanma',
                        'Uluslararası hat genişlemesi',
                        'Operasyonel verimlilik artışı',
                        'Yakıt fiyat riski'
                    ],
                    'technical_indicators': {
                        'rsi': 65.2,
                        'macd_signal': 'BUY',
                        'moving_avg_20': 235.80,
                        'moving_avg_50': 228.40,
                        'trend': 'BULLISH'
                    },
                    'news_sentiment': 'POSITIVE'
                },
                'ASELS.IS': {
                    'symbol': 'ASELS.IS',
                    'name': 'Aselsan',
                    'current_price': 89.75,
                    'recommendation': 'STRONG_BUY',
                    'recommendation_text': 'Güçlü Al',
                    'risk_level': 'HIGH',
                    'risk_text': 'Yüksek Risk',
                    'confidence_score': 85.2,
                    'target_price': 115.00,
                    'stop_loss_price': 75.00,
                    'analysis_text': 'Aselsan, savunma sektöründeki güçlü konumu ve teknolojik üstünlüğü ile dikkat çekiyor. İhracat artışı ve yeni sözleşmeler büyüme potansiyelini destekliyor.',
                    'key_factors': [
                        'Teknolojik liderlik',
                        'İhracat artışı',
                        'Yeni savunma projeleri',
                        'Devlet politikası riski'
                    ],
                    'technical_indicators': {
                        'rsi': 72.4,
                        'macd_signal': 'BUY',
                        'moving_avg_20': 82.30,
                        'moving_avg_50': 78.90,
                        'trend': 'BULLISH'
                    },
                    'news_sentiment': 'POSITIVE'
                },
                'AKBNK.IS': {
                    'symbol': 'AKBNK.IS',
                    'name': 'Akbank',
                    'current_price': 58.20,
                    'recommendation': 'HOLD',
                    'recommendation_text': 'Tut',
                    'risk_level': 'MEDIUM',
                    'risk_text': 'Orta Risk',
                    'confidence_score': 72.8,
                    'target_price': 65.50,
                    'stop_loss_price': 52.00,
                    'analysis_text': 'Akbank, Türkiye\'nin önde gelen bankalarından biri olarak sağlam finansal yapısı ile dikkat çekiyor. Kredi büyümesi ve net faiz marjındaki iyileşme olumlu. Ancak makroekonomik riskler takip edilmeli.',
                    'key_factors': [
                        'Güçlü bilanço yapısı',
                        'Kredi büyümesi',
                        'Dijital bankacılık yatırımları',
                        'Makroekonomik riskler'
                    ],
                    'technical_indicators': {
                        'rsi': 58.6,
                        'macd_signal': 'HOLD',
                        'moving_avg_20': 59.10,
                        'moving_avg_50': 61.20,
                        'trend': 'SIDEWAYS'
                    },
                    'news_sentiment': 'NEUTRAL'
                },
                'GARAN.IS': {
                    'symbol': 'GARAN.IS',
                    'name': 'Garanti Bankası',
                    'current_price': 93.45,
                    'recommendation': 'BUY',
                    'recommendation_text': 'Al',
                    'risk_level': 'MEDIUM',
                    'risk_text': 'Orta Risk',
                    'confidence_score': 76.3,
                    'target_price': 105.00,
                    'stop_loss_price': 85.00,
                    'analysis_text': 'Garanti Bankası, güçlü teknoloji altyapısı ve müşteri tabanı ile öne çıkıyor. Şirket bankacılığındaki büyüme ve dijital dönüşüm yatırımları değer yaratıyor.',
                    'key_factors': [
                        'Teknoloji liderliği',
                        'Şirket bankacılığı büyümesi',
                        'Güçlü müşteri tabanı',
                        'Düzenleyici riskler'
                    ],
                    'technical_indicators': {
                        'rsi': 63.8,
                        'macd_signal': 'BUY',
                        'moving_avg_20': 89.70,
                        'moving_avg_50': 87.30,
                        'trend': 'BULLISH'
                    },
                    'news_sentiment': 'POSITIVE'
                },
                'ISCTR.IS': {
                    'symbol': 'ISCTR.IS',
                    'name': 'İş Bankası',
                    'current_price': 12.85,
                    'recommendation': 'HOLD',
                    'recommendation_text': 'Tut',
                    'risk_level': 'LOW',
                    'risk_text': 'Düşük Risk',
                    'confidence_score': 68.4,
                    'target_price': 14.20,
                    'stop_loss_price': 11.50,
                    'analysis_text': 'İş Bankası, Türkiye\'nin köklü bankalarından biri olarak istikrarlı performans sergiliyor. Mevduat tabanının güçlü olması ve geniş şube ağı avantaj sağlıyor.',
                    'key_factors': [
                        'Güçlü mevduat tabanı',
                        'Geniş şube ağı',
                        'İstikrarlı karlılık',
                        'Rekabet baskısı'
                    ],
                    'technical_indicators': {
                        'rsi': 52.3,
                        'macd_signal': 'HOLD',
                        'moving_avg_20': 12.95,
                        'moving_avg_50': 13.10,
                        'trend': 'SIDEWAYS'
                    },
                    'news_sentiment': 'NEUTRAL'
                },
                'KCHOL.IS': {
                    'symbol': 'KCHOL.IS',
                    'name': 'Koç Holding',
                    'current_price': 156.20,
                    'recommendation': 'BUY',
                    'recommendation_text': 'Al',
                    'risk_level': 'MEDIUM',
                    'risk_text': 'Orta Risk',
                    'confidence_score': 81.7,
                    'target_price': 180.00,
                    'stop_loss_price': 140.00,
                    'analysis_text': 'Koç Holding, diversifiye iş portföyü ile Türkiye ekonomisinin lokomotifi konumunda. Otomotiv, enerji ve dayanıklı tüketim sektörlerindeki güçlü varlığı değer yaratıyor.',
                    'key_factors': [
                        'Diversifiye portföy',
                        'Güçlü yönetim',
                        'Sektör liderliği',
                        'Döngüsel riskler'
                    ],
                    'technical_indicators': {
                        'rsi': 67.9,
                        'macd_signal': 'BUY',
                        'moving_avg_20': 150.40,
                        'moving_avg_50': 145.80,
                        'trend': 'BULLISH'
                    },
                    'news_sentiment': 'POSITIVE'
                }
            }
            
            analysis = mock_analyses.get(symbol, {
                'symbol': symbol,
                'name': 'Analiz Bulunamadı',
                'error': f'{symbol} için detaylı analiz henüz mevcut değil'
            })
            
            return Response(analysis)
            
        except Exception as e:
            print(f"Stock analysis error: {e}")
            return Response({
                'error': 'Hisse analizi yapılırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class MarketOverviewView(APIView):
    """Piyasa genel durumu endpoint'i"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Genel piyasa durumunu getir"""
        try:
            mock_overview = {
                'bist100': {
                    'value': 8456.78,
                    'change': 125.45,
                    'change_percent': 1.51,
                    'volume': 185000000000,
                    'status': 'RISING'
                },
                'usd_try': {
                    'value': 34.15,
                    'change': -0.25,
                    'change_percent': -0.73,
                    'status': 'FALLING'
                },
                'trending_sectors': [
                    {'name': 'Teknoloji', 'change_percent': 4.2},
                    {'name': 'Savunma', 'change_percent': 3.8},
                    {'name': 'Enerji', 'change_percent': 2.5}
                ],
                'top_gainers': [
                    {'symbol': 'ASELS.IS', 'name': 'Aselsan', 'change_percent': 5.15},
                    {'symbol': 'TUPRS.IS', 'name': 'Tüpraş', 'change_percent': 4.35},
                    {'symbol': 'THYAO.IS', 'name': 'THY', 'change_percent': 3.25}
                ],
                'top_losers': [
                    {'symbol': 'AKBNK.IS', 'name': 'Akbank', 'change_percent': -1.85},
                    {'symbol': 'BIMAS.IS', 'name': 'BİM', 'change_percent': -0.65}
                ]
            }
            
            return Response(mock_overview)
            
        except Exception as e:
            print(f"Market overview error: {e}")
            return Response({
                'error': 'Piyasa durumu alınırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class UltraStockAnalysisView(APIView):
    """Ultra gelişmiş hisse analizi endpoint'i"""
    permission_classes = [AllowAny]  # Geçici test için
    
    def post(self, request):
        """Ultra detaylı AI hisse analizi"""
        try:
            symbol = request.data.get('symbol', '').strip().upper()
            
            if not symbol:
                return Response({
                    'error': 'Hisse sembolü gerekli (örn: THYAO.IS)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Ultra mock analiz verisi
            ultra_analyses = {
                'THYAO.IS': {
                    'success': True,
                    'symbol': 'THYAO.IS',
                    'current_price': 245.50,
                    'ai_analysis': {
                        'recommendation': 'STRONG_BUY',
                        'confidence_score': 87.5,
                        'target_price': 295.00,
                        'risk_level': 'MEDIUM',
                        'investment_thesis': 'THY, küresel havacılık sektöründeki toparlanmadan en fazla faydalanacak şirketlerden biri. Hub stratejisi, güçlü finansal yapı ve operasyonel mükemmellik odaklı yönetim yaklaşımı ile uzun vadeli değer yaratma potansiyeli yüksek.',
                        'key_metrics': {
                            'pe_ratio': 8.5,
                            'pb_ratio': 1.2,
                            'debt_equity': 0.65,
                            'roe': 18.5
                        }
                    },
                    'technical_analysis': {
                        'rsi': 68.5,
                        'macd': {
                            'signal': 'BULLISH',
                            'histogram': 2.15
                        },
                        'bollinger_bands': {
                            'upper': 265.00,
                            'middle': 240.00,
                            'lower': 215.00
                        },
                        'support_levels': [230.00, 220.00, 210.00],
                        'resistance_levels': [255.00, 270.00, 285.00],
                        'trend_analysis': 'GÜÇLÜ YUKSELİŞ'
                    },
                    'fundamental_analysis': {
                        'pe_ratio': 8.5,
                        'pb_ratio': 1.2,
                        'market_cap': 3380000000,
                        'fundamental_score': 85.2
                    },
                    'risk_metrics': {
                        'volatility': 0.285,
                        'var_95': -0.08,
                        'sharpe_ratio': 1.45,
                        'max_drawdown': -0.15,
                        'risk_category': 'ORTA'
                    },
                    'ai_insights': {
                        'pros': [
                            'Hub stratejisinin başarılı uygulanması',
                            'Güçlü operasyonel verimlilik',
                            'Turizm sektörü toparlanması',
                            'Teknolojik yatırımlar'
                        ],
                        'cons': [
                            'Yakıt fiyat volatilitesi',
                            'Jeopolitik riskler',
                            'Regülasyon riskleri'
                        ],
                        'catalysts': [
                            'Uluslararası seyahat artışı',
                            'Yeni destinasyon açılışları',
                            'Kargo segmenti büyümesi'
                        ],
                        'risks': [
                            'Küresel ekonomik yavaşlama',
                            'Havacılık krizleri',
                            'Döviz kuru riski'
                        ]
                    }
                },
                'ASELS.IS': {
                    'success': True,
                    'symbol': 'ASELS.IS',
                    'current_price': 89.75,
                    'ai_analysis': {
                        'recommendation': 'STRONG_BUY',
                        'confidence_score': 92.3,
                        'target_price': 125.00,
                        'risk_level': 'HIGH',
                        'investment_thesis': 'Aselsan, savunma teknolojilerinde Türkiye\'nin lider şirketi olarak, artan jeopolitik gerginlikler ve savunma harcamalarından faydalanacak. AR-GE odaklı büyüme stratejisi ve ihracat artışı değer yaratıyor.',
                        'key_metrics': {
                            'pe_ratio': 12.8,
                            'pb_ratio': 2.1,
                            'debt_equity': 0.35,
                            'roe': 22.5
                        }
                    },
                    'technical_analysis': {
                        'rsi': 75.2,
                        'macd': {
                            'signal': 'STRONG_BULLISH',
                            'histogram': 3.85
                        },
                        'bollinger_bands': {
                            'upper': 95.00,
                            'middle': 85.00,
                            'lower': 75.00
                        },
                        'support_levels': [82.00, 78.00, 72.00],
                        'resistance_levels': [95.00, 105.00, 118.00],
                        'trend_analysis': 'GÜÇLÜ YUKSELİŞ'
                    },
                    'fundamental_analysis': {
                        'pe_ratio': 12.8,
                        'pb_ratio': 2.1,
                        'market_cap': 196450000000,
                        'fundamental_score': 90.5
                    },
                    'risk_metrics': {
                        'volatility': 0.385,
                        'var_95': -0.12,
                        'sharpe_ratio': 1.75,
                        'max_drawdown': -0.22,
                        'risk_category': 'YÜKSEK'
                    },
                    'ai_insights': {
                        'pros': [
                            'Teknolojik üstünlük',
                            'Güçlü AR-GE kabiliyeti',
                            'İhracat artışı',
                            'Devlet desteği'
                        ],
                        'cons': [
                            'Yüksek volatilite',
                            'Politik risk',
                            'Tek sektör bağımlılığı'
                        ],
                        'catalysts': [
                            'Yeni savunma projeleri',
                            'İhracat anlaşmaları',
                            'Teknoloji transferleri'
                        ],
                        'risks': [
                            'Jeopolitik değişiklikler',
                            'Bütçe kısıtlamaları',
                            'Rekabet artışı'
                        ]
                    }
                },
                'BIMAS.IS': {
                    'success': True,
                    'symbol': 'BIMAS.IS',
                    'current_price': 485.00,
                    'ai_analysis': {
                        'recommendation': 'BUY',
                        'confidence_score': 78.9,
                        'target_price': 525.00,
                        'risk_level': 'LOW',
                        'investment_thesis': 'BİM, Türkiye perakende sektöründe güçlü konumu ve sürdürülebilir büyüme modeli ile öne çıkıyor. Şehir dışı yatırımlar ve dijital dönüşüm projeleri gelecekteki büyümeyi destekliyor.',
                        'key_metrics': {
                            'pe_ratio': 15.2,
                            'pb_ratio': 3.8,
                            'debt_equity': 0.25,
                            'roe': 25.8
                        }
                    },
                    'technical_analysis': {
                        'rsi': 45.8,
                        'macd': {
                            'signal': 'NEUTRAL',
                            'histogram': -0.25
                        },
                        'bollinger_bands': {
                            'upper': 510.00,
                            'middle': 485.00,
                            'lower': 460.00
                        },
                        'support_levels': [470.00, 455.00, 440.00],
                        'resistance_levels': [500.00, 515.00, 530.00],
                        'trend_analysis': 'YAN YÖN'
                    },
                    'fundamental_analysis': {
                        'pe_ratio': 15.2,
                        'pb_ratio': 3.8,
                        'market_cap': 329550000000,
                        'fundamental_score': 82.1
                    },
                    'risk_metrics': {
                        'volatility': 0.225,
                        'var_95': -0.06,
                        'sharpe_ratio': 1.25,
                        'max_drawdown': -0.18,
                        'risk_category': 'DÜŞÜK'
                    },
                    'ai_insights': {
                        'pros': [
                            'Güçlü pazar konumu',
                            'Sürdürülebilir büyüme',
                            'Operasyonel mükemmellik',
                            'Güçlü nakit yaratma'
                        ],
                        'cons': [
                            'Yoğun rekabet',
                            'Maliyet baskıları',
                            'Regulasyon riskleri'
                        ],
                        'catalysts': [
                            'Yeni mağaza açılışları',
                            'Dijital yatırımlar',
                            'E-ticaret büyümesi'
                        ],
                        'risks': [
                            'Tüketici harcama düşüşü',
                            'Enflasyon baskısı',
                            'Tedarik zinciri sorunları'
                        ]
                    }
                }
            }
            
            # Default analiz
            default_analysis = {
                'success': True,
                'symbol': symbol,
                'current_price': 100.00,
                'ai_analysis': {
                    'recommendation': 'HOLD',
                    'confidence_score': 65.0,
                    'target_price': 110.00,
                    'risk_level': 'MEDIUM',
                    'investment_thesis': f'{symbol} için detaylı analiz henüz hazır değil. Genel piyasa koşulları ve teknik göstergeler değerlendirildiğinde orta vadeli tutma stratejisi öneriliyor.',
                    'key_metrics': {}
                },
                'technical_analysis': {
                    'rsi': 50.0,
                    'macd': {'signal': 'NEUTRAL', 'histogram': 0.0},
                    'bollinger_bands': {'upper': 110.0, 'middle': 100.0, 'lower': 90.0},
                    'support_levels': [95.0, 90.0, 85.0],
                    'resistance_levels': [105.0, 110.0, 115.0],
                    'trend_analysis': 'NÖTR'
                },
                'fundamental_analysis': {
                    'pe_ratio': 15.0,
                    'pb_ratio': 1.5,
                    'market_cap': 1000000000,
                    'fundamental_score': 70.0
                },
                'risk_metrics': {
                    'volatility': 0.25,
                    'var_95': -0.05,
                    'sharpe_ratio': 1.0,
                    'max_drawdown': -0.20,
                    'risk_category': 'ORTA'
                },
                'ai_insights': {
                    'pros': ['Sektör ortalaması performans', 'Makul değerleme'],
                    'cons': ['Sınırlı büyüme potansiyeli', 'Piyasa belirsizlikleri'],
                    'catalysts': ['Genel piyasa iyileşmesi'],
                    'risks': ['Makroekonomik riskler']
                }
            }
            
            analysis = ultra_analyses.get(symbol, default_analysis)
            analysis['timestamp'] = datetime.now().isoformat()
            
            return Response(analysis)
            
        except Exception as e:
            print(f"Ultra stock analysis error: {e}")
            return Response({
                'error': 'Ultra hisse analizi yapılırken hata oluştu',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class PortfolioOptimizerView(APIView):
    """Portföy optimizasyonu endpoint'i"""
    permission_classes = [AllowAny]  # Geçici test için
    
    def post(self, request):
        """Modern Portföy Teorisi ile portföy optimizasyonu"""
        try:
            stocks = request.data.get('stocks', [])
            investment_amount = request.data.get('investment_amount', 100000)
            risk_tolerance = request.data.get('risk_tolerance', 'moderate')
            
            # Mock portföy optimizasyonu
            mock_optimization = {
                'success': True,
                'optimized_allocation': {
                    'THYAO.IS': 0.25,
                    'ASELS.IS': 0.20,
                    'AKBNK.IS': 0.15,
                    'GARAN.IS': 0.15,
                    'BIMAS.IS': 0.25
                },
                'expected_return': 0.145,  # 14.5%
                'expected_risk': 0.185,    # 18.5%
                'sharpe_ratio': 0.78,
                'risk_score': 7.2,
                'diversification_analysis': {
                    'sector_distribution': {
                        'Havayolu': 0.25,
                        'Savunma': 0.20,
                        'Bankacılık': 0.30,
                        'Perakende': 0.25
                    },
                    'concentration_risk': 'DÜŞÜK',
                    'risk_warnings': []
                },
                'rebalancing_suggestions': [
                    {
                        'symbol': 'THYAO.IS',
                        'current_weight': 0.30,
                        'suggested_weight': 0.25,
                        'action': 'AZALT'
                    }
                ]
            }
            
            return Response(mock_optimization)
            
        except Exception as e:
            print(f"Portfolio optimization error: {e}")
            return Response({
                'error': 'Portföy optimizasyonu yapılırken hata oluştu',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class MarketSentimentView(APIView):
    """Piyasa sentiment analizi endpoint'i"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Piyasa sentiment analizi"""
        try:
            mock_sentiment = {
                'success': True,
                'overall_sentiment': {
                    'score': 0.72,
                    'label': 'POZİTİF',
                    'confidence': 0.85
                },
                'fear_greed_index': {
                    'value': 68,
                    'label': 'AÇGÖZLÜLÜK',
                    'components': {
                        'price_momentum': 75,
                        'volatility': 45,
                        'volume': 65,
                        'social_sentiment': 80
                    }
                },
                'sector_sentiments': {
                    'teknoloji': {'score': 0.78, 'trend': 'YUKSELİŞ'},
                    'bankacılık': {'score': 0.65, 'trend': 'YAN YÖN'},
                    'enerji': {'score': 0.82, 'trend': 'YUKSELİŞ'},
                    'savunma': {'score': 0.88, 'trend': 'GÜÇLÜ YUKSELİŞ'},
                    'perakende': {'score': 0.58, 'trend': 'YAN YÖN'}
                },
                'news_analysis': {
                    'total_articles': 1250,
                    'positive_ratio': 0.68,
                    'negative_ratio': 0.22,
                    'key_themes': ['ekonomik toparlanma', 'teknoloji yatırımları', 'ihracat artışı']
                },
                'market_indicators': {
                    'vix_level': 18.5,
                    'trend_strength': 0.75,
                    'momentum': 'POZİTİF'
                }
            }
            
            return Response(mock_sentiment)
            
        except Exception as e:
            print(f"Market sentiment error: {e}")
            return Response({
                'error': 'Piyasa sentiment analizi yapılırken hata oluştu',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StockScreenerView(APIView):
    """Hisse tarama endpoint'i"""
    permission_classes = [AllowAny]  # Geçici test için
    
    def post(self, request):
        """AI destekli hisse tarama"""
        try:
            criteria = request.data.get('criteria', {})
            
            mock_screener = {
                'success': True,
                'recommendations': [
                    {
                        'symbol': 'ASELS.IS',
                        'name': 'Aselsan',
                        'ai_score': 92,
                        'recommendation': 'STRONG_BUY',
                        'current_price': 89.75,
                        'target_price': 125.00,
                        'upside_potential': 39.2,
                        'risk_level': 'HIGH',
                        'investment_thesis': 'Savunma teknolojilerinde lider konumu ve artan jeopolitik gerilimlerden faydalanacak.',
                        'key_factors': ['Teknolojik üstünlük', 'İhracat artışı', 'AR-GE yatırımları'],
                        'suggested_allocation': 0.20
                    },
                    {
                        'symbol': 'THYAO.IS',
                        'name': 'Türk Hava Yolları',
                        'ai_score': 87,
                        'recommendation': 'STRONG_BUY',
                        'current_price': 245.50,
                        'target_price': 295.00,
                        'upside_potential': 20.2,
                        'risk_level': 'MEDIUM',
                        'investment_thesis': 'Küresel havacılık sektöründeki toparlanmadan en fazla faydalanacak.',
                        'key_factors': ['Hub stratejisi', 'Operasyonel verimlilik', 'Turizm toparlanması'],
                        'suggested_allocation': 0.25
                    }
                ],
                'screening_criteria': criteria,
                'total_found': 2
            }
            
            return Response(mock_screener)
            
        except Exception as e:
            print(f"Stock screener error: {e}")
            return Response({
                'error': 'Hisse tarama yapılırken hata oluştu',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class AlertsView(APIView):
    """Uyarılar endpoint'i"""
    permission_classes = [AllowAny]  # Geçici test için
    
    def get(self, request):
        """Kullanıcı uyarılarını getir"""
        try:
            mock_alerts = {
                'success': True,
                'alerts': [
                    {
                        'id': '1',
                        'type': 'PRICE_ALERT',
                        'symbol': 'THYAO.IS',
                        'message': 'THY 250 TL seviyesini aştı!',
                        'priority': 'HIGH',
                        'created_at': datetime.now().isoformat(),
                        'is_active': True
                    },
                    {
                        'id': '2',
                        'type': 'TECHNICAL_SIGNAL',
                        'symbol': 'ASELS.IS',
                        'message': 'ASELS için güçlü alım sinyali oluştu',
                        'priority': 'MEDIUM',
                        'created_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                        'is_active': True
                    }
                ]
            }
            
            return Response(mock_alerts)
            
        except Exception as e:
            print(f"Alerts error: {e}")
            return Response({
                'error': 'Uyarılar alınırken hata oluştu',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
