"""
Finobai - Ultra Gelişmiş Borsa AI Analiz Motoru
Bu servis, gelişmiş yapay zeka algoritmaları ile borsa analizi yapar.
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Any, Optional, Tuple
import yfinance as yf
import requests
import openai
from django.conf import settings
from django.utils import timezone
from dataclasses import dataclass

from .models import (
    StockSymbol, StockPrice, StockAnalysis, UserPortfolio, 
    UserRiskProfile, PortfolioPosition
)


@dataclass
class MarketSentiment:
    """Piyasa sentiment verisi"""
    overall_sentiment: float  # -1 ile 1 arası
    fear_greed_index: float   # 0-100 arası
    volatility_index: float   # VIX benzeri
    news_sentiment: str       # POSITIVE/NEGATIVE/NEUTRAL
    social_sentiment: float   # Sosyal medya sentiment
    
    
@dataclass
class TechnicalIndicators:
    """Teknik analiz göstergeleri"""
    rsi: float
    macd: float
    macd_signal: float
    bollinger_upper: float
    bollinger_lower: float
    sma_20: float
    sma_50: float
    sma_200: float
    volume_sma: float
    stochastic_k: float
    stochastic_d: float
    atr: float  # Average True Range
    adx: float  # Average Directional Index
    

@dataclass
class FundamentalData:
    """Temel analiz verileri"""
    pe_ratio: float
    pb_ratio: float
    debt_to_equity: float
    roe: float
    roa: float
    profit_margin: float
    revenue_growth: float
    earnings_growth: float
    dividend_yield: float
    market_cap: float


class AdvancedAIStockAnalyzer:
    """Ultra gelişmiş AI borsa analiz motoru"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.risk_free_rate = 0.12  # Türkiye 10 yıllık tahvil faizi
    
    def analyze_stock_comprehensive(self, symbol: str, user_profile: Optional[UserRiskProfile] = None) -> Dict[str, Any]:
        """Kapsamlı hisse analizi (Teknik + Fundamental + AI)"""
        try:
            # 1. Veri toplama
            stock_data = self._fetch_comprehensive_data(symbol)
            if not stock_data:
                return self._generate_error_response(f"Veri bulunamadı: {symbol}")
            
            # 2. Teknik analiz
            technical_analysis = self._perform_technical_analysis(stock_data['price_history'])
            
            # 3. Fundamental analiz
            fundamental_analysis = self._perform_fundamental_analysis(stock_data['fundamental_data'])
            
            # 4. Sentiment analizi
            sentiment_analysis = self._analyze_market_sentiment(symbol)
            
            # 5. AI destekli değerlendirme
            ai_evaluation = self._generate_ai_evaluation(
                symbol, technical_analysis, fundamental_analysis, 
                sentiment_analysis, user_profile
            )
            
            # 6. Risk analizi
            risk_analysis = self._calculate_risk_metrics(stock_data['price_history'])
            
            # 7. Hedef fiyat hesaplama
            target_prices = self._calculate_target_prices(
                stock_data['current_price'], technical_analysis, 
                fundamental_analysis, ai_evaluation
            )
            
            # 8. Portföy uygunluk skoru
            portfolio_fit_score = self._calculate_portfolio_fit(symbol, user_profile) if user_profile else None
            
            # 9. Kapsamlı rapor oluştur
            comprehensive_report = {
                'symbol': symbol,
                'company_name': stock_data.get('company_name', ''),
                'current_price': stock_data['current_price'],
                'analysis_timestamp': datetime.now().isoformat(),
                'market_status': self._get_market_status(),
                
                # AI Değerlendirme
                'ai_recommendation': ai_evaluation['recommendation'],
                'confidence_score': ai_evaluation['confidence'],
                'ai_summary': ai_evaluation['summary'],
                'investment_thesis': ai_evaluation['investment_thesis'],
                
                # Teknik Analiz
                'technical_analysis': {
                    'overall_signal': technical_analysis['overall_signal'],
                    'strength': technical_analysis['signal_strength'],
                    'indicators': technical_analysis['indicators'],
                    'support_resistance': technical_analysis['support_resistance'],
                    'trend_analysis': technical_analysis['trend_analysis']
                },
                
                # Fundamental Analiz
                'fundamental_analysis': {
                    'valuation_score': fundamental_analysis['valuation_score'],
                    'financial_health': fundamental_analysis['financial_health'],
                    'growth_metrics': fundamental_analysis['growth_metrics'],
                    'profitability_metrics': fundamental_analysis['profitability_metrics']
                },
                
                # Risk Analizi
                'risk_analysis': {
                    'overall_risk': risk_analysis['overall_risk'],
                    'volatility': risk_analysis['volatility'],
                    'beta': risk_analysis['beta'],
                    'var_95': risk_analysis['var_95'],  # Value at Risk
                    'max_drawdown': risk_analysis['max_drawdown'],
                    'sharpe_ratio': risk_analysis['sharpe_ratio']
                },
                
                # Sentiment
                'sentiment_analysis': {
                    'news_sentiment': sentiment_analysis['news_sentiment'],
                    'social_sentiment': sentiment_analysis['social_sentiment'],
                    'analyst_sentiment': sentiment_analysis['analyst_sentiment'],
                    'overall_sentiment': sentiment_analysis['overall_sentiment']
                },
                
                # Hedef Fiyatlar
                'price_targets': {
                    'conservative': target_prices['conservative'],
                    'moderate': target_prices['moderate'],
                    'optimistic': target_prices['optimistic'],
                    'stop_loss': target_prices['stop_loss'],
                    'timeframe': target_prices['timeframe']
                },
                
                # Kullanıcı Uygunluğu
                'user_suitability': portfolio_fit_score,
                
                # Eylem Planı
                'action_plan': self._generate_action_plan(ai_evaluation, risk_analysis, user_profile),
                
                # Uyarılar
                'warnings': self._generate_warnings(risk_analysis, sentiment_analysis, user_profile)
            }
            
            return comprehensive_report
            
        except Exception as e:
            print(f"Comprehensive analysis error for {symbol}: {e}")
            return self._generate_error_response(f"Analiz hatası: {str(e)}")
    
    def _fetch_comprehensive_data(self, symbol: str) -> Optional[Dict]:
        """Kapsamlı veri çekme"""
        try:
            # Yahoo Finance'dan veri çek
            ticker = yf.Ticker(symbol)
            
            # Fiyat geçmişi (1 yıl)
            hist = ticker.history(period="1y", interval="1d")
            if hist.empty:
                return None
                
            # Temel veriler
            info = ticker.info
            
            # Son fiyat verileri
            latest = hist.iloc[-1]
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', symbol),
                'current_price': float(latest['Close']),
                'price_history': hist,
                'fundamental_data': info,
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A')
            }
            
        except Exception as e:
            print(f"Data fetch error for {symbol}: {e}")
            return None
    
    def _perform_technical_analysis(self, price_data: pd.DataFrame) -> Dict[str, Any]:
        """Detaylı teknik analiz"""
        try:
            # Temel fiyat verileri
            closes = price_data['Close'].values
            highs = price_data['High'].values
            lows = price_data['Low'].values
            volumes = price_data['Volume'].values
            
            # Hareketli ortalamalar
            sma_20 = np.mean(closes[-20:])
            sma_50 = np.mean(closes[-50:]) if len(closes) >= 50 else sma_20
            sma_200 = np.mean(closes[-200:]) if len(closes) >= 200 else sma_50
            
            # RSI hesaplama
            rsi = self._calculate_rsi(closes)
            
            # MACD hesaplama
            macd, macd_signal = self._calculate_macd(closes)
            
            # Bollinger Bands
            bb_upper, bb_lower = self._calculate_bollinger_bands(closes)
            
            # Support/Resistance seviyeleri
            support, resistance = self._find_support_resistance(highs, lows)
            
            # Trend analizi
            trend = self._analyze_trend(closes, sma_20, sma_50, sma_200)
            
            # Genel sinyal
            signals = []
            
            # RSI sinyali
            if rsi < 30:
                signals.append(('BUY', 0.7, 'RSI oversold'))
            elif rsi > 70:
                signals.append(('SELL', 0.7, 'RSI overbought'))
            else:
                signals.append(('NEUTRAL', 0.3, 'RSI normal'))
            
            # MACD sinyali
            if macd > macd_signal:
                signals.append(('BUY', 0.6, 'MACD pozitif'))
            else:
                signals.append(('SELL', 0.6, 'MACD negatif'))
            
            # Moving Average sinyali
            current_price = closes[-1]
            if current_price > sma_20 > sma_50:
                signals.append(('BUY', 0.8, 'Fiyat MA üstünde'))
            elif current_price < sma_20 < sma_50:
                signals.append(('SELL', 0.8, 'Fiyat MA altında'))
            
            # Genel sinyal hesaplama
            buy_strength = sum([s[1] for s in signals if s[0] == 'BUY'])
            sell_strength = sum([s[1] for s in signals if s[0] == 'SELL'])
            
            if buy_strength > sell_strength:
                overall_signal = 'BUY'
                signal_strength = min(buy_strength / (buy_strength + sell_strength) * 100, 100)
            elif sell_strength > buy_strength:
                overall_signal = 'SELL' 
                signal_strength = min(sell_strength / (buy_strength + sell_strength) * 100, 100)
            else:
                overall_signal = 'HOLD'
                signal_strength = 50
            
            return {
                'overall_signal': overall_signal,
                'signal_strength': round(signal_strength, 1),
                'indicators': {
                    'rsi': round(rsi, 2),
                    'macd': round(macd, 4),
                    'macd_signal': round(macd_signal, 4),
                    'sma_20': round(sma_20, 2),
                    'sma_50': round(sma_50, 2),
                    'sma_200': round(sma_200, 2),
                    'bollinger_upper': round(bb_upper, 2),
                    'bollinger_lower': round(bb_lower, 2)
                },
                'support_resistance': {
                    'support': round(support, 2),
                    'resistance': round(resistance, 2)
                },
                'trend_analysis': trend,
                'detailed_signals': signals
            }
            
        except Exception as e:
            print(f"Technical analysis error: {e}")
            return self._get_default_technical_analysis()
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """RSI hesaplama"""
        if len(prices) < period + 1:
            return 50.0
            
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: np.ndarray) -> Tuple[float, float]:
        """MACD hesaplama"""
        if len(prices) < 26:
            return 0.0, 0.0
            
        ema_12 = self._calculate_ema(prices, 12)
        ema_26 = self._calculate_ema(prices, 26)
        macd = ema_12 - ema_26
        
        # MACD signal line (MACD'nin 9 günlük EMA'sı)
        macd_values = []
        for i in range(26, len(prices)):
            ema_12_i = self._calculate_ema(prices[:i+1], 12)
            ema_26_i = self._calculate_ema(prices[:i+1], 26)
            macd_values.append(ema_12_i - ema_26_i)
        
        if len(macd_values) >= 9:
            signal = self._calculate_ema(np.array(macd_values), 9)
        else:
            signal = macd
            
        return macd, signal
    
    def _calculate_ema(self, prices: np.ndarray, period: int) -> float:
        """EMA hesaplama"""
        if len(prices) < period:
            return np.mean(prices)
            
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
            
        return ema
    
    def _calculate_bollinger_bands(self, prices: np.ndarray, period: int = 20) -> Tuple[float, float]:
        """Bollinger Bands hesaplama"""
        if len(prices) < period:
            return prices[-1] * 1.02, prices[-1] * 0.98
            
        sma = np.mean(prices[-period:])
        std = np.std(prices[-period:])
        
        upper = sma + (2 * std)
        lower = sma - (2 * std)
        
        return upper, lower
    
    def _find_support_resistance(self, highs: np.ndarray, lows: np.ndarray) -> Tuple[float, float]:
        """Support/Resistance seviyeleri"""
        # Son 50 günün verilerini kullan
        recent_highs = highs[-50:] if len(highs) >= 50 else highs
        recent_lows = lows[-50:] if len(lows) >= 50 else lows
        
        # Resistance: Son dönemin en yüksek değerlerinin ortalaması
        top_highs = np.sort(recent_highs)[-5:]  # En yüksek 5 değer
        resistance = np.mean(top_highs)
        
        # Support: Son dönemin en düşük değerlerinin ortalaması  
        bottom_lows = np.sort(recent_lows)[:5]  # En düşük 5 değer
        support = np.mean(bottom_lows)
        
        return support, resistance
    
    def _analyze_trend(self, prices: np.ndarray, sma_20: float, sma_50: float, sma_200: float) -> Dict[str, Any]:
        """Trend analizi"""
        current_price = prices[-1]
        
        # Kısa vadeli trend (son 20 gün)
        if len(prices) >= 20:
            short_trend = "BULLISH" if current_price > sma_20 else "BEARISH"
            short_strength = abs(current_price - sma_20) / sma_20 * 100
        else:
            short_trend = "NEUTRAL"
            short_strength = 0
        
        # Orta vadeli trend (son 50 gün)
        if len(prices) >= 50:
            medium_trend = "BULLISH" if sma_20 > sma_50 else "BEARISH"
            medium_strength = abs(sma_20 - sma_50) / sma_50 * 100
        else:
            medium_trend = "NEUTRAL"  
            medium_strength = 0
        
        # Uzun vadeli trend (son 200 gün)
        if len(prices) >= 200:
            long_trend = "BULLISH" if sma_50 > sma_200 else "BEARISH"
            long_strength = abs(sma_50 - sma_200) / sma_200 * 100
        else:
            long_trend = "NEUTRAL"
            long_strength = 0
        
        # Genel trend
        trends = [short_trend, medium_trend, long_trend]
        if trends.count("BULLISH") >= 2:
            overall_trend = "BULLISH"
        elif trends.count("BEARISH") >= 2:
            overall_trend = "BEARISH"
        else:
            overall_trend = "NEUTRAL"
        
        return {
            'overall_trend': overall_trend,
            'short_term': {'direction': short_trend, 'strength': round(short_strength, 2)},
            'medium_term': {'direction': medium_trend, 'strength': round(medium_strength, 2)},
            'long_term': {'direction': long_trend, 'strength': round(long_strength, 2)}
        }
    
    def _perform_fundamental_analysis(self, fundamental_data: Dict) -> Dict[str, Any]:
        """Fundamental analiz"""
        try:
            # Temel metrikler
            pe_ratio = fundamental_data.get('forwardPE', fundamental_data.get('trailingPE', 0))
            pb_ratio = fundamental_data.get('priceToBook', 0)
            debt_to_equity = fundamental_data.get('debtToEquity', 0)
            roe = fundamental_data.get('returnOnEquity', 0)
            profit_margin = fundamental_data.get('profitMargins', 0)
            revenue_growth = fundamental_data.get('revenueGrowth', 0)
            
            # Değerleme skoru (0-100)
            valuation_score = self._calculate_valuation_score(pe_ratio, pb_ratio, roe)
            
            # Finansal sağlık skoru
            financial_health = self._calculate_financial_health_score(debt_to_equity, roe, profit_margin)
            
            # Büyüme metrikleri
            growth_metrics = {
                'revenue_growth': revenue_growth * 100 if revenue_growth else 0,
                'earnings_growth': fundamental_data.get('earningsGrowth', 0) * 100,
                'growth_score': self._calculate_growth_score(revenue_growth)
            }
            
            # Karlılık metrikleri
            profitability_metrics = {
                'roe': roe * 100 if roe else 0,
                'roa': fundamental_data.get('returnOnAssets', 0) * 100,
                'profit_margin': profit_margin * 100 if profit_margin else 0,
                'profitability_score': self._calculate_profitability_score(roe, profit_margin)
            }
            
            return {
                'valuation_score': valuation_score,
                'financial_health': financial_health,
                'growth_metrics': growth_metrics,
                'profitability_metrics': profitability_metrics,
                'key_ratios': {
                    'pe_ratio': pe_ratio or 0,
                    'pb_ratio': pb_ratio or 0,
                    'debt_to_equity': debt_to_equity or 0
                }
            }
            
        except Exception as e:
            print(f"Fundamental analysis error: {e}")
            return self._get_default_fundamental_analysis()
    
    def _calculate_valuation_score(self, pe_ratio: float, pb_ratio: float, roe: float) -> int:
        """Değerleme skoru hesaplama (0-100)"""
        score = 50  # Başlangıç puanı
        
        # P/E ratio değerlendirme
        if pe_ratio > 0:
            if pe_ratio < 10:
                score += 20  # Düşük P/E iyi
            elif pe_ratio < 15:
                score += 10
            elif pe_ratio > 30:
                score -= 15  # Yüksek P/E kötü
            elif pe_ratio > 25:
                score -= 5
        
        # P/B ratio değerlendirme
        if pb_ratio > 0:
            if pb_ratio < 1:
                score += 15  # Düşük P/B iyi
            elif pb_ratio < 2:
                score += 5
            elif pb_ratio > 5:
                score -= 10  # Yüksek P/B kötü
        
        # ROE ile düzeltme
        if roe > 0:
            if roe > 0.20:  # %20 üstü ROE mükemmel
                score += 15
            elif roe > 0.15:
                score += 10
            elif roe < 0.05:
                score -= 15  # %5 altı ROE kötü
        
        return max(0, min(100, score))
    
    def _calculate_financial_health_score(self, debt_to_equity: float, roe: float, profit_margin: float) -> int:
        """Finansal sağlık skoru"""
        score = 50
        
        # Borç/Özkaynak oranı
        if debt_to_equity > 0:
            if debt_to_equity < 0.3:
                score += 20  # Düşük borç iyi
            elif debt_to_equity < 0.6:
                score += 10
            elif debt_to_equity > 1.5:
                score -= 20  # Yüksek borç kötü
            elif debt_to_equity > 1:
                score -= 10
        
        # Karlılık metrikleri
        if roe > 0.15:
            score += 15
        elif roe < 0:
            score -= 25
        
        if profit_margin > 0.10:
            score += 15
        elif profit_margin < 0:
            score -= 20
        
        return max(0, min(100, score))
    
    def _calculate_growth_score(self, revenue_growth: float) -> int:
        """Büyüme skoru"""
        if not revenue_growth:
            return 30
            
        growth_pct = revenue_growth * 100
        
        if growth_pct > 20:
            return 90
        elif growth_pct > 10:
            return 75
        elif growth_pct > 5:
            return 60
        elif growth_pct > 0:
            return 45
        else:
            return 20
    
    def _calculate_profitability_score(self, roe: float, profit_margin: float) -> int:
        """Karlılık skoru"""
        score = 0
        
        if roe:
            if roe > 0.20:
                score += 50
            elif roe > 0.15:
                score += 40
            elif roe > 0.10:
                score += 25
            elif roe > 0:
                score += 10
        
        if profit_margin:
            if profit_margin > 0.15:
                score += 50
            elif profit_margin > 0.10:
                score += 35
            elif profit_margin > 0.05:
                score += 20
            elif profit_margin > 0:
                score += 10
        
        return min(100, score)
    
    def _analyze_market_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Piyasa sentiment analizi"""
        # Basit mock sentiment - gerçek uygulamada news API'ları kullanılacak
        sentiments = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
        import random
        
        news_sentiment = random.choice(sentiments)
        social_sentiment = random.uniform(-1, 1)
        analyst_sentiment = random.choice(sentiments)
        
        # Genel sentiment skoru
        sentiment_score = 0
        if news_sentiment == 'POSITIVE':
            sentiment_score += 0.4
        elif news_sentiment == 'NEGATIVE':
            sentiment_score -= 0.4
            
        sentiment_score += social_sentiment * 0.3
        
        if analyst_sentiment == 'POSITIVE':
            sentiment_score += 0.3
        elif analyst_sentiment == 'NEGATIVE':
            sentiment_score -= 0.3
        
        # -1 ile 1 arası normalize et
        sentiment_score = max(-1, min(1, sentiment_score))
        
        if sentiment_score > 0.3:
            overall_sentiment = 'POSITIVE'
        elif sentiment_score < -0.3:
            overall_sentiment = 'NEGATIVE'
        else:
            overall_sentiment = 'NEUTRAL'
        
        return {
            'news_sentiment': news_sentiment,
            'social_sentiment': round(social_sentiment, 2),
            'analyst_sentiment': analyst_sentiment,
            'overall_sentiment': overall_sentiment,
            'sentiment_score': round(sentiment_score, 2)
        }
    
    def _generate_ai_evaluation(self, symbol: str, technical: Dict, fundamental: Dict, 
                               sentiment: Dict, user_profile: Optional[UserRiskProfile]) -> Dict[str, Any]:
        """AI destekli kapsamlı değerlendirme"""
        try:
            # Kullanıcı profil bilgilerini hazırla
            user_context = ""
            if user_profile:
                user_context = f"""
                Kullanıcı Profili:
                - Risk Toleransı: {user_profile.risk_tolerance}
                - Yatırım Hedefi: {user_profile.investment_goal}
                - Yatırım Vadesi: {user_profile.investment_horizon} ay
                - Aylık Bütçe: {user_profile.monthly_investment_budget}₺
                - Deneyim: {user_profile.experience_years} yıl
                """
            
            # AI analiz promptu
            prompt = f"""
            {symbol} hissesi için ultra detaylı yatırım analizi yap:
            
            TEKNİK ANALİZ:
            - Genel Sinyal: {technical['overall_signal']} (%{technical['signal_strength']} güç)
            - RSI: {technical['indicators']['rsi']}
            - MACD: {technical['indicators']['macd']}
            - Trend: {technical['trend_analysis']['overall_trend']}
            - Support: {technical['support_resistance']['support']}
            - Resistance: {technical['support_resistance']['resistance']}
            
            FUNDAMENTAL ANALİZ:
            - Değerleme Skoru: {fundamental['valuation_score']}/100
            - Finansal Sağlık: {fundamental['financial_health']}/100
            - Büyüme Skoru: {fundamental['growth_metrics']['growth_score']}/100
            - Karlılık Skoru: {fundamental['profitability_metrics']['profitability_score']}/100
            
            SENTIMENT ANALİZ:
            - Haber Sentiment: {sentiment['news_sentiment']}
            - Sosyal Sentiment: {sentiment['social_sentiment']}
            - Genel Sentiment: {sentiment['overall_sentiment']}
            
            {user_context}
            
            JSON formatında yanıt ver:
            {{
                "recommendation": "STRONG_BUY/BUY/HOLD/SELL/STRONG_SELL",
                "confidence": 85,
                "summary": "3 cümlelik özet değerlendirme",
                "investment_thesis": "Yatırım tezi - neden bu tavsiyeyi veriyorsun",
                "strengths": ["güçlü yön 1", "güçlü yön 2", "güçlü yön 3"],
                "weaknesses": ["zayıf yön 1", "zayıf yön 2"],
                "catalysts": ["olumlu katalizör 1", "olumlu katalizör 2"],
                "risks": ["risk faktörü 1", "risk faktörü 2"],
                "time_horizon": "KISA/ORTA/UZUN",
                "allocation_suggestion": 15,
                "monitoring_points": ["takip edilecek metrik 1", "takip edilecek metrik 2"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen dünya çapında deneyimli bir yatırım analisti ve portföy yöneticisisin. Türkiye piyasalarında uzman ve kullanıcılara kişiselleştirilmiş yatırım tavsiyeleri veriyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            ai_analysis = json.loads(response.choices[0].message.content)
            return ai_analysis
            
        except Exception as e:
            print(f"AI evaluation error: {e}")
            return self._get_fallback_ai_evaluation(technical, fundamental)
    
    def _calculate_risk_metrics(self, price_data: pd.DataFrame) -> Dict[str, Any]:
        """Risk metrik hesaplamaları"""
        try:
            returns = price_data['Close'].pct_change().dropna()
            
            # Volatilite (yıllık)
            daily_vol = returns.std()
            annual_vol = daily_vol * np.sqrt(252)
            
            # Beta (BIST 100'e karşı, basitleştirilmiş)
            # Gerçek uygulamada BIST 100 verisi çekilmeli
            beta = 1.0  # Varsayılan beta
            
            # Value at Risk (95% güven aralığı)
            var_95 = np.percentile(returns, 5) * 100
            
            # Maximum Drawdown
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min() * 100
            
            # Sharpe Ratio
            excess_returns = returns.mean() - (self.risk_free_rate / 252)
            sharpe_ratio = excess_returns / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
            
            # Risk seviyesi belirleme
            if annual_vol < 0.15:
                risk_level = "DÜŞÜK"
            elif annual_vol < 0.25:
                risk_level = "ORTA"
            elif annual_vol < 0.40:
                risk_level = "YÜKSEK"
            else:
                risk_level = "ÇOK YÜKSEK"
            
            return {
                'overall_risk': risk_level,
                'volatility': round(annual_vol * 100, 2),  # Yüzde olarak
                'beta': round(beta, 2),
                'var_95': round(var_95, 2),
                'max_drawdown': round(max_drawdown, 2),
                'sharpe_ratio': round(sharpe_ratio, 2)
            }
            
        except Exception as e:
            print(f"Risk calculation error: {e}")
            return {
                'overall_risk': 'ORTA',
                'volatility': 25.0,
                'beta': 1.0,
                'var_95': -5.0,
                'max_drawdown': -20.0,
                'sharpe_ratio': 0.5
            }
    
    def _calculate_target_prices(self, current_price: float, technical: Dict, 
                                fundamental: Dict, ai_eval: Dict) -> Dict[str, Any]:
        """Hedef fiyat hesaplamaları"""
        
        # Teknik analiz hedefleri
        resistance = technical['support_resistance']['resistance']
        support = technical['support_resistance']['support']
        
        # AI tavsiyesine göre çarpanlar
        recommendation = ai_eval.get('recommendation', 'HOLD')
        confidence = ai_eval.get('confidence', 50) / 100
        
        if recommendation in ['STRONG_BUY', 'BUY']:
            optimistic_multiplier = 1.15 + (confidence * 0.1)
            moderate_multiplier = 1.08 + (confidence * 0.05)
            conservative_multiplier = 1.03 + (confidence * 0.02)
        elif recommendation in ['STRONG_SELL', 'SELL']:
            optimistic_multiplier = 0.85 - (confidence * 0.1)
            moderate_multiplier = 0.92 - (confidence * 0.05)
            conservative_multiplier = 0.97 - (confidence * 0.02)
        else:  # HOLD
            optimistic_multiplier = 1.05
            moderate_multiplier = 1.02
            conservative_multiplier = 0.98
        
        # Hedef fiyatları hesapla
        optimistic = current_price * optimistic_multiplier
        moderate = current_price * moderate_multiplier
        conservative = current_price * conservative_multiplier
        
        # Stop loss (teknik analiz destekli)
        if recommendation in ['BUY', 'STRONG_BUY']:
            stop_loss = min(support * 0.95, current_price * 0.92)
        else:
            stop_loss = current_price * 0.95
        
        # Zaman dilimi
        if ai_eval.get('time_horizon') == 'KISA':
            timeframe = "1-3 ay"
        elif ai_eval.get('time_horizon') == 'ORTA':
            timeframe = "3-12 ay"
        else:
            timeframe = "12+ ay"
        
        return {
            'conservative': round(conservative, 2),
            'moderate': round(moderate, 2),
            'optimistic': round(optimistic, 2),
            'stop_loss': round(stop_loss, 2),
            'timeframe': timeframe,
            'upside_potential': round((optimistic - current_price) / current_price * 100, 1),
            'downside_risk': round((stop_loss - current_price) / current_price * 100, 1)
        }
    
    def _calculate_portfolio_fit(self, symbol: str, user_profile: UserRiskProfile) -> Dict[str, Any]:
        """Kullanıcı portföyüne uygunluk skoru"""
        if not user_profile:
            return None
        
        fit_score = 50  # Başlangıç skoru
        reasons = []
        
        # Risk toleransına uygunluk
        stock_risk = self._estimate_stock_risk_level(symbol)
        
        if user_profile.risk_tolerance == 'CONSERVATIVE':
            if stock_risk in ['DÜŞÜK', 'ORTA']:
                fit_score += 20
                reasons.append("Risk seviyesi profilinize uygun")
            else:
                fit_score -= 30
                reasons.append("Risk seviyesi çok yüksek")
        elif user_profile.risk_tolerance == 'AGGRESSIVE':
            if stock_risk in ['YÜKSEK', 'ÇOK YÜKSEK']:
                fit_score += 25
                reasons.append("Yüksek risk profilinize uygun")
            else:
                fit_score += 5
                reasons.append("Risk seviyesi düşük olabilir")
        
        # Yatırım hedefine uygunluk
        if user_profile.investment_goal == 'CAPITAL_PRESERVATION' and stock_risk in ['DÜŞÜK', 'ORTA']:
            fit_score += 15
            reasons.append("Sermaye koruma hedefi için uygun")
        elif user_profile.investment_goal == 'AGGRESSIVE_GROWTH' and stock_risk in ['YÜKSEK', 'ÇOK YÜKSEK']:
            fit_score += 20
            reasons.append("Agresif büyüme hedefi için ideal")
        
        # Sektör tercihine uygunluk
        # Bu kısım gerçek uygulamada sektör bilgisi ile geliştirilecek
        
        # Uygunluk seviyesi
        if fit_score >= 80:
            suitability = "ÇOK UYGUN"
        elif fit_score >= 65:
            suitability = "UYGUN"
        elif fit_score >= 45:
            suitability = "KISMEN UYGUN"
        else:
            suitability = "UYGUN DEĞİL"
        
        # Önerilen alokasyon
        if suitability == "ÇOK UYGUN":
            suggested_allocation = min(15, user_profile.monthly_investment_budget / 1000 * 2)
        elif suitability == "UYGUN":
            suggested_allocation = min(10, user_profile.monthly_investment_budget / 1000 * 1.5)
        elif suitability == "KISMEN UYGUN":
            suggested_allocation = min(5, user_profile.monthly_investment_budget / 1000 * 1)
        else:
            suggested_allocation = 0
        
        return {
            'fit_score': max(0, min(100, fit_score)),
            'suitability': suitability,
            'suggested_allocation_percent': round(suggested_allocation, 1),
            'reasons': reasons,
            'warnings': self._generate_suitability_warnings(fit_score, user_profile)
        }
    
    def _estimate_stock_risk_level(self, symbol: str) -> str:
        """Hisse risk seviyesi tahmini"""
        # Sektör bazlı basit risk tahmini
        if 'BANK' in symbol or any(bank in symbol for bank in ['AKBNK', 'GARAN', 'ISCTR', 'VAKBN']):
            return 'ORTA'
        elif any(tech in symbol for tech in ['ASELS', 'TCELL']):
            return 'YÜKSEK'
        elif any(stable in symbol for stable in ['BIMAS', 'MGROS']):
            return 'DÜŞÜK'
        else:
            return 'ORTA'
    
    def _generate_action_plan(self, ai_eval: Dict, risk_analysis: Dict, 
                             user_profile: Optional[UserRiskProfile]) -> List[str]:
        """Eylem planı oluştur"""
        actions = []
        
        recommendation = ai_eval.get('recommendation', 'HOLD')
        
        if recommendation in ['STRONG_BUY', 'BUY']:
            actions.append("📈 Kademeli alım stratejisi uygulayın")
            actions.append("📊 Hedef fiyatlara kadar bekleyin")
            actions.append("⚠️ Stop-loss seviyenizi belirleyin")
            
            if user_profile and user_profile.experience_years < 2:
                actions.append("🎓 Küçük pozisyonla başlayın ve deneyim kazanın")
                
        elif recommendation in ['STRONG_SELL', 'SELL']:
            actions.append("📉 Mevcut pozisyonları gözden geçirin")
            actions.append("💰 Kâr realizasyonu düşünün")
            actions.append("🔍 Alternatif yatırım araçlarını araştırın")
            
        else:  # HOLD
            actions.append("⏳ Mevcut pozisyonu koruyun")
            actions.append("📈 Teknik seviyeleri takip edin")
            actions.append("📰 Şirket haberlerini izleyin")
        
        # Risk seviyesine göre ek eylemler
        if risk_analysis['overall_risk'] in ['YÜKSEK', 'ÇOK YÜKSEK']:
            actions.append("⚠️ Portföy çeşitlendirmesi yapın")
            actions.append("🛡️ Pozisyon büyüklüğünü sınırlayın")
        
        return actions
    
    def _generate_warnings(self, risk_analysis: Dict, sentiment_analysis: Dict, 
                          user_profile: Optional[UserRiskProfile]) -> List[str]:
        """Uyarı mesajları oluştur"""
        warnings = []
        
        # Risk uyarıları
        if risk_analysis['volatility'] > 40:
            warnings.append("⚠️ Yüksek volatilite - fiyat dalgalanmaları beklenebilir")
            
        if risk_analysis['max_drawdown'] < -30:
            warnings.append("📉 Geçmişte %30+ değer kaybı yaşamış")
            
        if risk_analysis['sharpe_ratio'] < 0:
            warnings.append("📊 Risk-getiri oranı olumsuz")
        
        # Sentiment uyarıları
        if sentiment_analysis['overall_sentiment'] == 'NEGATIVE':
            warnings.append("😰 Olumsuz piyasa sentimenti")
            
        # Kullanıcı profil uyarıları
        if user_profile:
            if user_profile.experience_years < 1:
                warnings.append("🔰 Yeni başlayan yatırımcı - dikkatli olun")
                
            if user_profile.risk_tolerance == 'CONSERVATIVE':
                warnings.append("🛡️ Muhafazakar profil - yüksek riskli yatırımlardan kaçının")
        
        return warnings
    
    def _get_market_status(self) -> str:
        """Piyasa durumu"""
        now = datetime.now()
        hour = now.hour
        
        # BIST işlem saatleri: 09:30 - 17:30
        if 9 <= hour <= 17:
            return "AÇIK"
        else:
            return "KAPALI"
    
    # Fallback metodları
    def _get_default_technical_analysis(self) -> Dict[str, Any]:
        """Varsayılan teknik analiz"""
        return {
            'overall_signal': 'HOLD',
            'signal_strength': 50.0,
            'indicators': {
                'rsi': 50.0,
                'macd': 0.0,
                'macd_signal': 0.0,
                'sma_20': 0.0,
                'sma_50': 0.0,
                'sma_200': 0.0,
                'bollinger_upper': 0.0,
                'bollinger_lower': 0.0
            },
            'support_resistance': {
                'support': 0.0,
                'resistance': 0.0
            },
            'trend_analysis': {
                'overall_trend': 'NEUTRAL',
                'short_term': {'direction': 'NEUTRAL', 'strength': 0},
                'medium_term': {'direction': 'NEUTRAL', 'strength': 0},
                'long_term': {'direction': 'NEUTRAL', 'strength': 0}
            }
        }
    
    def _get_default_fundamental_analysis(self) -> Dict[str, Any]:
        """Varsayılan fundamental analiz"""
        return {
            'valuation_score': 50,
            'financial_health': 50,
            'growth_metrics': {
                'revenue_growth': 0,
                'earnings_growth': 0,
                'growth_score': 50
            },
            'profitability_metrics': {
                'roe': 0,
                'roa': 0,
                'profit_margin': 0,
                'profitability_score': 50
            },
            'key_ratios': {
                'pe_ratio': 0,
                'pb_ratio': 0,
                'debt_to_equity': 0
            }
        }
    
    def _get_fallback_ai_evaluation(self, technical: Dict, fundamental: Dict) -> Dict[str, Any]:
        """AI analiz başarısız olduğunda fallback"""
        # Teknik ve fundamental skorlara göre basit karar
        tech_signal = technical['overall_signal']
        fund_score = (fundamental['valuation_score'] + fundamental['financial_health']) / 2
        
        if tech_signal == 'BUY' and fund_score > 60:
            recommendation = 'BUY'
            confidence = 70
        elif tech_signal == 'SELL' or fund_score < 40:
            recommendation = 'SELL' 
            confidence = 65
        else:
            recommendation = 'HOLD'
            confidence = 55
        
        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'summary': f"Teknik analiz {tech_signal} sinyali, fundamental skor {fund_score}/100",
            'investment_thesis': "Detaylı AI analizi şu anda mevcut değil. Teknik ve fundamental göstergeler baz alınmıştır.",
            'strengths': ["Analiz devam ediyor"],
            'weaknesses': ["Detaylı analiz gerekli"],
            'catalysts': ["Gelecek dönem sonuçları"],
            'risks': ["Piyasa volatilitesi"],
            'time_horizon': 'ORTA',
            'allocation_suggestion': 5,
            'monitoring_points': ["Fiyat hareketleri", "Temel göstergeler"]
        }
    
    def _generate_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Hata yanıtı"""
        return {
            'error': True,
            'message': error_msg,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_suitability_warnings(self, fit_score: int, user_profile: UserRiskProfile) -> List[str]:
        """Uygunluk uyarıları"""
        warnings = []
        
        if fit_score < 50:
            warnings.append("Bu hisse risk profilinize uygun olmayabilir")
            
        if user_profile.experience_years < 2 and fit_score < 70:
            warnings.append("Deneyim seviyeniz göz önünde bulundurularak dikkatli olun")
            
        return warnings


# Portföy optimizasyon servisi
class PortfolioOptimizerService:
    """Modern Portföy Teorisi ile optimizasyon"""
    
    def __init__(self):
        self.analyzer = AdvancedAIStockAnalyzer()
    
    def optimize_portfolio(self, user_profile: UserRiskProfile, 
                          available_stocks: List[str]) -> Dict[str, Any]:
        """Kullanıcı profiline göre optimal portföy oluştur"""
        
        # Her hisse için analiz yap
        stock_analyses = {}
        for symbol in available_stocks:
            analysis = self.analyzer.analyze_stock_comprehensive(symbol, user_profile)
            if not analysis.get('error'):
                stock_analyses[symbol] = analysis
        
        # Risk-getiri optimizasyonu
        optimal_weights = self._calculate_optimal_weights(stock_analyses, user_profile)
        
        # Portföy performans metrikleri
        portfolio_metrics = self._calculate_portfolio_metrics(optimal_weights, stock_analyses)
        
        # Çeşitlendirme analizi
        diversification_analysis = self._analyze_diversification(optimal_weights, stock_analyses)
        
        return {
            'optimal_allocation': optimal_weights,
            'portfolio_metrics': portfolio_metrics,
            'diversification': diversification_analysis,
            'rebalancing_schedule': self._suggest_rebalancing_schedule(user_profile),
            'risk_budget': self._calculate_risk_budget(optimal_weights, stock_analyses),
            'expected_returns': portfolio_metrics['expected_annual_return'],
            'max_drawdown_estimate': portfolio_metrics['estimated_max_drawdown']
        }
    
    def _calculate_optimal_weights(self, analyses: Dict, user_profile: UserRiskProfile) -> Dict[str, float]:
        """Optimal ağırlık hesaplama"""
        # Basitleştirilmiş optimizasyon - gerçek uygulamada scipy.optimize kullanılmalı
        
        total_score = 0
        stock_scores = {}
        
        # Her hisse için toplam skor hesapla
        for symbol, analysis in analyses.items():
            # AI tavsiye skoru
            rec_score = self._recommendation_to_score(analysis['ai_recommendation'])
            
            # Güven skoru
            confidence = analysis['confidence_score'] / 100
            
            # Uygunluk skoru
            suitability = analysis.get('user_suitability', {}).get('fit_score', 50) / 100
            
            # Toplam skor
            score = rec_score * confidence * suitability
            stock_scores[symbol] = score
            total_score += score
        
        # Ağırlıkları hesapla
        optimal_weights = {}
        for symbol, score in stock_scores.items():
            weight = (score / total_score) * 100 if total_score > 0 else 0
            optimal_weights[symbol] = round(weight, 2)
        
        return optimal_weights
    
    def _recommendation_to_score(self, recommendation: str) -> float:
        """Tavsiye skoruna çevir"""
        scores = {
            'STRONG_BUY': 1.0,
            'BUY': 0.8,
            'HOLD': 0.5,
            'SELL': 0.2,
            'STRONG_SELL': 0.1
        }
        return scores.get(recommendation, 0.5)
    
    def _calculate_portfolio_metrics(self, weights: Dict, analyses: Dict) -> Dict[str, Any]:
        """Portföy performans metrikleri"""
        # Ağırlıklı ortalama hesaplamaları
        weighted_confidence = sum(
            weights.get(symbol, 0) * analyses[symbol]['confidence_score'] 
            for symbol in analyses
        ) / 100
        
        weighted_risk = sum(
            weights.get(symbol, 0) * self._risk_to_numeric(analyses[symbol]['risk_analysis']['overall_risk'])
            for symbol in analyses
        ) / 100
        
        return {
            'expected_annual_return': round(weighted_confidence * 0.15, 2),  # Basitleştirilmiş
            'portfolio_risk_score': round(weighted_risk, 1),
            'estimated_volatility': round(weighted_risk * 0.3, 2),
            'estimated_max_drawdown': round(weighted_risk * 0.25, 2),
            'diversification_ratio': len([w for w in weights.values() if w > 5]) / len(weights)
        }
    
    def _risk_to_numeric(self, risk_level: str) -> float:
        """Risk seviyesini sayısal değere çevir"""
        levels = {
            'DÜŞÜK': 25,
            'ORTA': 50,
            'YÜKSEK': 75,
            'ÇOK YÜKSEK': 90
        }
        return levels.get(risk_level, 50)
    
    def _analyze_diversification(self, weights: Dict, analyses: Dict) -> Dict[str, Any]:
        """Çeşitlendirme analizi"""
        # Sektör dağılımı analizi (basitleştirilmiş)
        sectors = {}
        for symbol, weight in weights.items():
            # Sektör bilgisini sembolden tahmin et - gerçek uygulamada API'den alınmalı
            sector = self._estimate_sector(symbol)
            sectors[sector] = sectors.get(sector, 0) + weight
        
        # Çeşitlendirme skoru
        concentration_risk = max(sectors.values()) if sectors else 0
        
        if concentration_risk > 50:
            diversification_score = 30
            diversification_status = "ZAYIF"
        elif concentration_risk > 30:
            diversification_score = 60
            diversification_status = "ORTA"
        else:
            diversification_score = 90
            diversification_status = "İYİ"
        
        return {
            'sector_allocation': sectors,
            'concentration_risk': round(concentration_risk, 2),
            'diversification_score': diversification_score,
            'diversification_status': diversification_status,
            'recommendations': self._get_diversification_recommendations(sectors)
        }
    
    def _estimate_sector(self, symbol: str) -> str:
        """Sembolden sektör tahmini"""
        if any(bank in symbol for bank in ['AKBNK', 'GARAN', 'ISCTR', 'VAKBN']):
            return 'Bankacılık'
        elif any(tech in symbol for tech in ['ASELS', 'TCELL']):
            return 'Teknoloji'
        elif any(retail in symbol for retail in ['BIMAS', 'MGROS']):
            return 'Perakende'
        elif any(energy in symbol for energy in ['TUPRS', 'PETKM']):
            return 'Enerji'
        elif 'THYAO' in symbol:
            return 'Ulaştırma'
        else:
            return 'Diğer'
    
    def _suggest_rebalancing_schedule(self, user_profile: UserRiskProfile) -> str:
        """Yeniden dengeleme önerisi"""
        if user_profile.risk_tolerance == 'CONSERVATIVE':
            return "6 ayda bir"
        elif user_profile.risk_tolerance == 'MODERATE':
            return "3 ayda bir"
        else:
            return "Aylık"
    
    def _calculate_risk_budget(self, weights: Dict, analyses: Dict) -> Dict[str, float]:
        """Risk bütçesi hesaplama"""
        risk_contributions = {}
        
        for symbol, weight in weights.items():
            if symbol in analyses:
                risk_level = self._risk_to_numeric(analyses[symbol]['risk_analysis']['overall_risk'])
                risk_contribution = weight * (risk_level / 100)
                risk_contributions[symbol] = round(risk_contribution, 2)
        
        return risk_contributions
    
    def _get_diversification_recommendations(self, sectors: Dict[str, float]) -> List[str]:
        """Çeşitlendirme önerileri"""
        recommendations = []
        
        max_sector = max(sectors, key=sectors.get) if sectors else None
        max_weight = max(sectors.values()) if sectors else 0
        
        if max_weight > 40:
            recommendations.append(f"{max_sector} sektöründeki ağırlığı azaltın")
            
        if len(sectors) < 4:
            recommendations.append("Farklı sektörlerden hisse ekleyin")
            
        if 'Bankacılık' not in sectors:
            recommendations.append("Bankacılık sektöründen hisse düşünün")
            
        return recommendations
