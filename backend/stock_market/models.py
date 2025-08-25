from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class StockSymbol(models.Model):
    """Borsa sembolleri ve hisse senetleri"""
    
    MARKET_CHOICES = [
        ('BIST', 'Borsa İstanbul'),
        ('NASDAQ', 'NASDAQ'),
        ('NYSE', 'New York Stock Exchange'),
        ('CRYPTO', 'Cryptocurrency'),
        ('FOREX', 'Foreign Exchange')
    ]
    
    symbol = models.CharField(max_length=20, unique=True)  # THYAO, AAPL, BTC-USD
    name = models.CharField(max_length=200)  # Türk Hava Yolları
    market = models.CharField(max_length=20, choices=MARKET_CHOICES)
    sector = models.CharField(max_length=100, blank=True)  # Havayolu, Teknoloji
    currency = models.CharField(max_length=10, default='TRY')  # TRY, USD, EUR
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['symbol']
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"


class StockPrice(models.Model):
    """Gerçek zamanlı hisse fiyatları"""
    
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE, related_name='prices')
    open_price = models.DecimalField(max_digits=10, decimal_places=4)
    current_price = models.DecimalField(max_digits=10, decimal_places=4)
    high_price = models.DecimalField(max_digits=10, decimal_places=4)
    low_price = models.DecimalField(max_digits=10, decimal_places=4)
    close_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    volume = models.BigIntegerField(default=0)
    change_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # %5.67
    change_amount = models.DecimalField(max_digits=10, decimal_places=4, default=0)  # 1.25
    market_cap = models.BigIntegerField(null=True, blank=True)  # Piyasa değeri
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        unique_together = ['stock', 'timestamp']
    
    def __str__(self):
        return f"{self.stock.symbol} - {self.current_price}"


class UserPortfolio(models.Model):
    """Kullanıcı portföyü"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_gain_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gain_loss_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Portfolio - {self.total_value}₺"


class PortfolioPosition(models.Model):
    """Portföydeki pozisyonlar"""
    
    portfolio = models.ForeignKey(UserPortfolio, on_delete=models.CASCADE, related_name='positions')
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)  # Hisse/coin miktarı
    average_cost = models.DecimalField(max_digits=10, decimal_places=4)  # Ortalama maliyet
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    invested_amount = models.DecimalField(max_digits=15, decimal_places=2)
    gain_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gain_loss_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['portfolio', 'stock']
    
    def __str__(self):
        return f"{self.portfolio.user.username} - {self.stock.symbol}: {self.quantity}"


class StockAnalysis(models.Model):
    """AI destekli hisse analizleri"""
    
    RECOMMENDATION_CHOICES = [
        ('STRONG_BUY', 'Güçlü Al'),
        ('BUY', 'Al'),
        ('HOLD', 'Tut'),
        ('SELL', 'Sat'),
        ('STRONG_SELL', 'Güçlü Sat')
    ]
    
    RISK_LEVELS = [
        ('LOW', 'Düşük Risk'),
        ('MEDIUM', 'Orta Risk'),
        ('HIGH', 'Yüksek Risk'),
        ('VERY_HIGH', 'Çok Yüksek Risk')
    ]
    
    stock = models.ForeignKey(StockSymbol, on_delete=models.CASCADE, related_name='analyses')
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100
    target_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    stop_loss_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Teknik analiz göstergeleri
    rsi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # RSI
    macd_signal = models.CharField(max_length=10, blank=True)  # BUY/SELL/NEUTRAL
    moving_avg_20 = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    moving_avg_50 = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # AI analiz sonucu
    analysis_text = models.TextField()  # AI'nin açıklaması
    key_factors = models.JSONField(default=list)  # Önemli faktörler
    news_sentiment = models.CharField(max_length=20, blank=True)  # POSITIVE/NEGATIVE/NEUTRAL
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.stock.symbol} - {self.recommendation}"


class MarketNews(models.Model):
    """Piyasa haberleri"""
    
    title = models.CharField(max_length=300)
    content = models.TextField()
    source = models.CharField(max_length=100)  # Reuters, Bloomberg, vs.
    url = models.URLField(blank=True)
    sentiment = models.CharField(max_length=20, blank=True)  # POSITIVE/NEGATIVE/NEUTRAL
    related_stocks = models.ManyToManyField(StockSymbol, blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title[:50]


class UserRiskProfile(models.Model):
    """Kullanıcı risk profili"""
    
    RISK_TOLERANCE_CHOICES = [
        ('CONSERVATIVE', 'Muhafazakar'),
        ('MODERATE', 'Orta Riskli'),
        ('AGGRESSIVE', 'Agresif'),
        ('VERY_AGGRESSIVE', 'Çok Agresif')
    ]
    
    INVESTMENT_GOALS = [
        ('CAPITAL_PRESERVATION', 'Sermaye Korunması'),
        ('INCOME_GENERATION', 'Gelir Üretimi'),
        ('BALANCED_GROWTH', 'Dengeli Büyüme'),
        ('AGGRESSIVE_GROWTH', 'Agresif Büyüme'),
        ('SPECULATION', 'Spekülatif Yatırım')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='risk_profile')
    risk_tolerance = models.CharField(max_length=20, choices=RISK_TOLERANCE_CHOICES)
    investment_goal = models.CharField(max_length=30, choices=INVESTMENT_GOALS)
    investment_horizon = models.IntegerField()  # Yatırım vadesi (ay)
    monthly_investment_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Yatırım deneyimi
    experience_years = models.IntegerField(default=0)
    previously_invested_instruments = models.JSONField(default=list)  # ['stocks', 'bonds', 'crypto']
    
    # Sektör tercihleri
    preferred_sectors = models.JSONField(default=list)
    avoided_sectors = models.JSONField(default=list)
    
    # Risk soruları sonuçları
    risk_score = models.IntegerField(default=0)  # 1-100 arası risk skoru
    quiz_results = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.risk_tolerance}"
