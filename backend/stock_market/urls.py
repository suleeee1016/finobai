from django.urls import path
from .views import (
    StockPricesView,
    StockAnalysisView, 
    MarketOverviewView,
    UltraStockAnalysisView,
    PortfolioOptimizerView,
    MarketSentimentView,
    StockScreenerView,
    AlertsView
)

urlpatterns = [
    # Temel endpoints
    path('prices/', StockPricesView.as_view(), name='stock_prices'),
    path('analyze/', StockAnalysisView.as_view(), name='stock_analysis'), 
    path('overview/', MarketOverviewView.as_view(), name='market_overview'),
    
    # Ultra gelişmiş AI endpoints
    path('ultra-analysis/', UltraStockAnalysisView.as_view(), name='ultra_stock_analysis'),
    path('portfolio-optimizer/', PortfolioOptimizerView.as_view(), name='portfolio_optimizer'),
    path('market-sentiment/', MarketSentimentView.as_view(), name='market_sentiment'),
    path('stock-screener/', StockScreenerView.as_view(), name='stock_screener'),
    path('alerts/', AlertsView.as_view(), name='alerts'),
]
