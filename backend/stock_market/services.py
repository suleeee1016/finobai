import json
import requests
import yfinance as yf
from datetime import datetime, timedelta
from decimal import Decimal
import openai
from django.conf import settings
from django.utils import timezone

from .models import StockSymbol, StockPrice, StockAnalysis, MarketNews, UserRiskProfile


class StockDataService:
    """Hisse senedi verilerini çeken servis"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def get_bist_stocks(self) -> list:
        """BIST 100 hisselerinin listesini getir"""
        # BIST 100'ün popüler hisseleri
        bist_stocks = [
            ('THYAO.IS', 'Türk Hava Yolları'),
            ('AKBNK.IS', 'Akbank'),
            ('GARAN.IS', 'Garanti BBVA'),
            ('VAKBN.IS', 'VakıfBank'),
            ('ISCTR.IS', 'İş Bankası'),
            ('ASELS.IS', 'Aselsan'),
            ('BIMAS.IS', 'BİM'),
            ('TUPRS.IS', 'Tüpraş'),
            ('SAHOL.IS', 'Sabancı Holding'),
            ('KCHOL.IS', 'Koç Holding'),
            ('PETKM.IS', 'Petkim'),
            ('TCELL.IS', 'Turkcell'),
            ('DOHOL.IS', 'Doğan Holding'),
            ('MGROS.IS', 'Migros'),
            ('ARCELIK.IS', 'Arçelik'),
        ]
        return bist_stocks
    
    def fetch_stock_price(self, symbol: str) -> dict:
        """Belirli bir hisse için güncel fiyat bilgisi getir"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2d")
            info = stock.info
            
            if hist.empty:
                return None
            
            latest = hist.iloc[-1]
            previous = hist.iloc[-2] if len(hist) > 1 else latest
            
            current_price = float(latest['Close'])
            open_price = float(latest['Open'])
            high_price = float(latest['High'])
            low_price = float(latest['Low'])
            volume = int(latest['Volume'])
            
            # Değişim hesapla
            change_amount = current_price - float(previous['Close'])
            change_percent = (change_amount / float(previous['Close'])) * 100
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'open_price': open_price,
                'high_price': high_price,
                'low_price': low_price,
                'volume': volume,
                'change_amount': change_amount,
                'change_percent': change_percent,
                'market_cap': info.get('marketCap', 0),
                'currency': 'TRY' if '.IS' in symbol else 'USD'
            }
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def update_all_stock_prices(self):
        """Tüm aktif hisselerin fiyatlarını güncelle"""
        symbols = StockSymbol.objects.filter(is_active=True)
        
        for stock_symbol in symbols:
            price_data = self.fetch_stock_price(stock_symbol.symbol)
            
            if price_data:
                StockPrice.objects.create(
                    stock=stock_symbol,
                    open_price=Decimal(str(price_data['open_price'])),
                    current_price=Decimal(str(price_data['current_price'])),
                    high_price=Decimal(str(price_data['high_price'])),
                    low_price=Decimal(str(price_data['low_price'])),
                    volume=price_data['volume'],
                    change_percent=Decimal(str(price_data['change_percent'])),
                    change_amount=Decimal(str(price_data['change_amount'])),
                    market_cap=price_data.get('market_cap'),
                )
    
    def get_trending_stocks(self) -> list:
        """Günün trend hisselerini getir"""
        # Son 24 saat içindeki en çok değişen hisseler
        recent_prices = StockPrice.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-change_percent')[:10]
        
        return recent_prices


class StockAnalysisService:
    """AI destekli hisse analiz servisi"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def analyze_stock(self, symbol: str) -> dict:
        """Hisse senedi için AI analizi yap"""
        try:
            # Hisse verisini al
            stock_data = StockDataService().fetch_stock_price(symbol)
            
            if not stock_data:
                return None
            
            # AI analiz promptu
            prompt = f"""
            Hisse senedi analiz uzmanı olarak {symbol} hissesini analiz et:
            
            Güncel Veriler:
            - Fiyat: {stock_data['current_price']}
            - Değişim: %{stock_data['change_percent']:.2f}
            - Hacim: {stock_data['volume']}
            - Piyasa Değeri: {stock_data.get('market_cap', 'N/A')}
            
            JSON formatında yanıt ver:
            {{
                "recommendation": "BUY/SELL/HOLD",
                "risk_level": "LOW/MEDIUM/HIGH/VERY_HIGH",
                "confidence": 85,
                "target_price": 125.50,
                "stop_loss": 95.00,
                "analysis": "Detaylı analiz açıklaması",
                "key_factors": ["faktör1", "faktör2", "faktör3"],
                "technical_indicators": {{
                    "rsi": 65.5,
                    "macd_signal": "BUY",
                    "trend": "BULLISH"
                }}
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen deneyimli bir finansal analist ve yatırım uzmanısın."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            print(f"AI analysis error for {symbol}: {e}")
            return self._get_fallback_analysis(stock_data)
    
    def _get_fallback_analysis(self, stock_data: dict) -> dict:
        """AI analiz başarısız olduğunda basit analiz"""
        change_percent = stock_data['change_percent']
        
        if change_percent > 5:
            recommendation = "BUY"
            risk_level = "MEDIUM"
        elif change_percent > 0:
            recommendation = "HOLD"
            risk_level = "LOW"
        elif change_percent > -5:
            recommendation = "HOLD"
            risk_level = "MEDIUM"
        else:
            recommendation = "SELL"
            risk_level = "HIGH"
        
        return {
            "recommendation": recommendation,
            "risk_level": risk_level,
            "confidence": 60,
            "target_price": stock_data['current_price'] * 1.1,
            "stop_loss": stock_data['current_price'] * 0.9,
            "analysis": f"Hisse %{change_percent:.2f} değişim gösteriyor. Teknik analizde daha detaylı inceleme gerekli.",
            "key_factors": ["Fiyat değişimi", "Piyasa trendi", "Hacim analizi"],
            "technical_indicators": {
                "rsi": 50,
                "macd_signal": "NEUTRAL",
                "trend": "SIDEWAYS"
            }
        }
    
    def generate_portfolio_recommendation(self, user_risk_profile: UserRiskProfile) -> dict:
        """Kullanıcı risk profiline göre portföy önerisi"""
        try:
            # Kullanıcı profiline göre prompt hazırla
            prompt = f"""
            Risk Profili: {user_risk_profile.risk_tolerance}
            Yatırım Hedefi: {user_risk_profile.investment_goal}
            Aylık Bütçe: {user_risk_profile.monthly_investment_budget}₺
            Yatırım Vade: {user_risk_profile.investment_horizon} ay
            Deneyim: {user_risk_profile.experience_years} yıl
            
            Bu profile uygun BIST ve global hisse portföyü öner.
            JSON formatında yanıt ver:
            {{
                "portfolio_allocation": {{
                    "stocks": 60,
                    "bonds": 30,
                    "cash": 10
                }},
                "recommended_stocks": [
                    {{"symbol": "THYAO.IS", "allocation": 15, "reason": "Nedenler"}},
                    {{"symbol": "AKBNK.IS", "allocation": 20, "reason": "Nedenler"}}
                ],
                "risk_warning": "Risk uyarısı",
                "expected_return": "8-12% yıllık",
                "rebalance_frequency": "3 ayda bir"
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen deneyimli bir portföy yöneticisisin."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.4
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Portfolio recommendation error: {e}")
            return self._get_default_portfolio_recommendation(user_risk_profile)
    
    def _get_default_portfolio_recommendation(self, risk_profile) -> dict:
        """Varsayılan portföy önerisi"""
        if risk_profile.risk_tolerance == 'CONSERVATIVE':
            return {
                "portfolio_allocation": {"stocks": 30, "bonds": 60, "cash": 10},
                "recommended_stocks": [
                    {"symbol": "VAKBN.IS", "allocation": 15, "reason": "İstikrarlı banka hissesi"},
                    {"symbol": "BIMAS.IS", "allocation": 15, "reason": "Savunma sektörü hissesi"}
                ],
                "risk_warning": "Muhafazakar yatırım stratejisi düşük risk içerir.",
                "expected_return": "5-8% yıllık",
                "rebalance_frequency": "6 ayda bir"
            }
        else:
            return {
                "portfolio_allocation": {"stocks": 70, "bonds": 20, "cash": 10},
                "recommended_stocks": [
                    {"symbol": "THYAO.IS", "allocation": 20, "reason": "Büyüme potansiyeli"},
                    {"symbol": "ASELS.IS", "allocation": 25, "reason": "Teknoloji lideri"},
                    {"symbol": "TUPRS.IS", "allocation": 25, "reason": "Enerji sektörü"}
                ],
                "risk_warning": "Agresif strateji yüksek risk içerir.",
                "expected_return": "10-15% yıllık",
                "rebalance_frequency": "3 ayda bir"
            }


class MarketNewsService:
    """Piyasa haberlerini çeken servis"""
    
    def fetch_market_news(self) -> list:
        """Güncel piyasa haberlerini çek"""
        # Gerçek uygulamada Reuters/Bloomberg API kullanılacak
        # Şimdilik mock veri
        mock_news = [
            {
                'title': 'BIST 100 Endeksi Yeni Rekor Kırdı',
                'content': 'Borsa İstanbul BIST 100 endeksi bugün 8,500 seviyesini aşarak tüm zamanların rekorunu kırdı...',
                'source': 'Finans Gündem',
                'sentiment': 'POSITIVE',
                'published_at': timezone.now() - timedelta(hours=2)
            },
            {
                'title': 'Merkez Bankası Faiz Kararı Açıklandı',
                'content': 'T.C. Merkez Bankası faiz oranlarını %45 seviyesinde sabit tuttu...',
                'source': 'Reuters Türkiye',
                'sentiment': 'NEUTRAL',
                'published_at': timezone.now() - timedelta(hours=4)
            },
            {
                'title': 'Teknoloji Hisselerinde Yükseliş Trendi',
                'content': 'ASELSAN ve Turkcell gibi teknoloji hisseleri son bir haftada %15 değer kazandı...',
                'source': 'Bloomberg HT',
                'sentiment': 'POSITIVE',
                'published_at': timezone.now() - timedelta(hours=6)
            }
        ]
        
        return mock_news
    
    def analyze_news_sentiment(self, news_text: str) -> str:
        """Haber metninin sentiment analizi"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Finansal haber sentiment analisti"},
                    {"role": "user", "content": f"Bu haberin piyasa sentiment'i nedir (POSITIVE/NEGATIVE/NEUTRAL): {news_text}"}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            sentiment = response.choices[0].message.content.strip().upper()
            return sentiment if sentiment in ['POSITIVE', 'NEGATIVE', 'NEUTRAL'] else 'NEUTRAL'
            
        except:
            return 'NEUTRAL'
