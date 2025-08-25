import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

interface StockData {
  symbol: string;
  name: string;
  current_price: number;
  change_percent: number;
  change_amount: number;
  volume: number;
  market_cap: number;
  sector: string;
  currency: string;
}

// Ultra Advanced Stock Analysis Interfaces
interface UltraStockAnalysis {
  success: boolean;
  symbol: string;
  current_price: number;
  ai_analysis: {
    recommendation: string;
    confidence_score: number;
    target_price: number;
    risk_level: string;
    investment_thesis: string;
    key_metrics: {
      [key: string]: any;
    };
  };
  technical_analysis: {
    rsi: number;
    macd: any;
    bollinger_bands: any;
    support_levels: number[];
    resistance_levels: number[];
    trend_analysis: string;
  };
  fundamental_analysis: {
    pe_ratio: number;
    pb_ratio: number;
    market_cap: number;
    fundamental_score: number;
  };
  risk_metrics: {
    volatility: number;
    var_95: number;
    sharpe_ratio: number;
    max_drawdown: number;
    risk_category: string;
  };
  ai_insights: {
    pros: string[];
    cons: string[];
    catalysts: string[];
    risks: string[];
  };
}

interface PortfolioOptimization {
  success: boolean;
  optimized_allocation: {
    [symbol: string]: number;
  };
  expected_return: number;
  expected_risk: number;
  sharpe_ratio: number;
  risk_score: number;
  diversification_analysis: {
    sector_distribution: {
      [sector: string]: number;
    };
    concentration_risk: string;
    risk_warnings: string[];
  };
  rebalancing_suggestions: Array<{
    symbol: string;
    current_weight: number;
    suggested_weight: number;
    action: string;
  }>;
}

interface MarketSentiment {
  success: boolean;
  overall_sentiment: {
    score: number;
    label: string;
    confidence: number;
  };
  fear_greed_index: {
    value: number;
    label: string;
    components: {
      [key: string]: number;
    };
  };
  sector_sentiments: {
    [sector: string]: {
      score: number;
      trend: string;
    };
  };
  news_analysis: {
    total_articles: number;
    positive_ratio: number;
    negative_ratio: number;
    key_themes: string[];
  };
  market_indicators: {
    vix_level: number;
    trend_strength: number;
    momentum: string;
  };
}

interface StockScreenerResult {
  success: boolean;
  recommendations: Array<{
    symbol: string;
    name: string;
    ai_score: number;
    recommendation: string;
    current_price: number;
    target_price: number;
    upside_potential: number;
    risk_level: string;
    investment_thesis: string;
    key_factors: string[];
    suggested_allocation: number;
  }>;
  screening_criteria: {
    market_cap_min: number;
    pe_ratio_max: number;
    debt_ratio_max: number;
    roa_min: number;
    risk_tolerance: string;
  };
  total_found: number;
}

interface AlertsResponse {
  success: boolean;
  alerts: Array<{
    id: string;
    type: string;
    symbol: string;
    message: string;
    priority: string;
    created_at: string;
    is_active: boolean;
  }>;
}

interface StockAnalysis {
  symbol: string;
  name: string;
  current_price: number;
  recommendation: string;
  recommendation_text: string;
  risk_level: string;
  risk_text: string;
  confidence_score: number;
  target_price: number;
  stop_loss_price: number;
  analysis_text: string;
  key_factors: string[];
  technical_indicators: {
    rsi: number;
    macd_signal: string;
    trend: string;
  };
  news_sentiment: string;
}

interface MarketOverview {
  bist100: {
    value: number;
    change: number;
    change_percent: number;
  };
  usd_try: {
    value: number;
    change: number;
    change_percent: number;
  };
  top_gainers: Array<{
    symbol: string;
    name: string;
    change_percent: number;
  }>;
  top_losers: Array<{
    symbol: string;
    name: string;
    change_percent: number;
  }>;
}

const StockMarketDashboard: React.FC = () => {
  const { user, token } = useAuth();
  
  // Existing states
  const [stocks, setStocks] = useState<StockData[]>([]);
  const [stockAnalysis, setStockAnalysis] = useState<StockAnalysis | null>(null);
  const [marketOverview, setMarketOverview] = useState<MarketOverview | null>(null);
  const [isLoadingStocks, setIsLoadingStocks] = useState(false);
  const [isLoadingAnalysis, setIsLoadingAnalysis] = useState(false);
  const [isLoadingOverview, setIsLoadingOverview] = useState(false);
  
  // New Ultra Advanced States
  const [ultraAnalysis, setUltraAnalysis] = useState<UltraStockAnalysis | null>(null);
  const [portfolioOptimization, setPortfolioOptimization] = useState<PortfolioOptimization | null>(null);
  const [marketSentiment, setMarketSentiment] = useState<MarketSentiment | null>(null);
  const [stockScreener, setStockScreener] = useState<StockScreenerResult | null>(null);
  const [alerts, setAlerts] = useState<AlertsResponse | null>(null);
  
  // Loading states for new features
  const [isLoadingUltraAnalysis, setIsLoadingUltraAnalysis] = useState(false);
  const [isLoadingPortfolio, setIsLoadingPortfolio] = useState(false);
  const [isLoadingSentiment, setIsLoadingSentiment] = useState(false);
  const [isLoadingScreener, setIsLoadingScreener] = useState(false);
  const [isLoadingAlerts, setIsLoadingAlerts] = useState(false);
  
  // Tab state - expanded with new tabs
  const [activeTab, setActiveTab] = useState<'overview' | 'stocks' | 'analysis' | 'ultra-analysis' | 'portfolio' | 'sentiment' | 'screener' | 'alerts'>('overview');
  
  // Form states for new features
  const [selectedStockForAnalysis, setSelectedStockForAnalysis] = useState('');
  const [portfolioStocks, setPortfolioStocks] = useState<string[]>(['THYAO.IS', 'AKBNK.IS', 'GARAN.IS', 'ASELS.IS']);
  const [screenerCriteria, setScreenerCriteria] = useState({
    market_cap_min: 1000000000, // 1B
    pe_ratio_max: 25,
    debt_ratio_max: 0.6,
    roa_min: 0.05,
    risk_tolerance: 'moderate'
  });

  // Ultra Advanced API Functions
  const performUltraStockAnalysis = async (symbol: string) => {
    if (!symbol) return;
    
    setIsLoadingUltraAnalysis(true);
    setUltraAnalysis(null);
    
    try {
      const response = await axios.post('http://localhost:8000/api/stocks/ultra-analysis/', 
        { symbol },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      setUltraAnalysis(response.data);
      setActiveTab('ultra-analysis');
    } catch (error: any) {
      console.error('Ultra analysis error:', error);
      alert(`Ultra analiz hatası: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsLoadingUltraAnalysis(false);
    }
  };

  const optimizePortfolio = async () => {
    setIsLoadingPortfolio(true);
    setPortfolioOptimization(null);
    
    try {
      const response = await axios.post('http://localhost:8000/api/stocks/portfolio-optimizer/', 
        { 
          stocks: portfolioStocks,
          investment_amount: 100000,
          risk_tolerance: 'moderate'
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      setPortfolioOptimization(response.data);
      setActiveTab('portfolio');
    } catch (error: any) {
      console.error('Portfolio optimization error:', error);
      alert(`Portföy optimizasyonu hatası: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsLoadingPortfolio(false);
    }
  };

  const fetchMarketSentiment = async () => {
    setIsLoadingSentiment(true);
    setMarketSentiment(null);
    
    try {
      const response = await axios.get('http://localhost:8000/api/stocks/market-sentiment/', {
        headers: { 'Content-Type': 'application/json' }
      });
      
      setMarketSentiment(response.data);
    } catch (error: any) {
      console.error('Market sentiment error:', error);
      alert(`Piyasa duygu durumu hatası: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsLoadingSentiment(false);
    }
  };

  const performStockScreening = async () => {
    setIsLoadingScreener(true);
    setStockScreener(null);
    
    try {
      const response = await axios.post('http://localhost:8000/api/stocks/stock-screener/', 
        { criteria: screenerCriteria },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      setStockScreener(response.data);
      setActiveTab('screener');
    } catch (error: any) {
      console.error('Stock screening error:', error);
      alert(`Hisse tarama hatası: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsLoadingScreener(false);
    }
  };

  const fetchAlerts = async () => {
    setIsLoadingAlerts(true);
    setAlerts(null);
    
    try {
      const response = await axios.get('http://localhost:8000/api/stocks/alerts/', {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      setAlerts(response.data);
    } catch (error: any) {
      console.error('Alerts fetch error:', error);
      alert(`Uyarı listesi hatası: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsLoadingAlerts(false);
    }
  };
  const loadStocks = async () => {
    setIsLoadingStocks(true);
    try {
      const response = await fetch('http://localhost:8000/api/stocks/prices/');
      if (!response.ok) throw new Error('Hisse verileri alınamadı');
      
      const data = await response.json();
      setStocks(data.stocks);
    } catch (error) {
      console.error('Stocks loading error:', error);
      alert('Hisse verileri yüklenirken hata oluştu!');
    } finally {
      setIsLoadingStocks(false);
    }
  };

  // Piyasa genel durumunu getir
  const loadMarketOverview = async () => {
    setIsLoadingOverview(true);
    try {
      const response = await fetch('http://localhost:8000/api/stocks/overview/');
      if (!response.ok) throw new Error('Piyasa verileri alınamadı');
      
      const data = await response.json();
      setMarketOverview(data);
    } catch (error) {
      console.error('Market overview loading error:', error);
      alert('Piyasa durumu yüklenirken hata oluştu!');
    } finally {
      setIsLoadingOverview(false);
    }
  };

  // Hisse analizi yap
  const analyzeStock = async (symbol: string) => {
    if (!symbol) return;
    
    setIsLoadingAnalysis(true);
    setStockAnalysis(null); // Önceki analizi temizle
    
    try {
      const response = await fetch('http://localhost:8000/api/stocks/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Hata kontrolü
      if (data.error) {
        alert(`Hisse analizi hatası: ${data.error}`);
        return;
      }
      
      setStockAnalysis(data);
      setActiveTab('analysis');
    } catch (error) {
      console.error('Stock analysis error:', error);
      alert('Hisse analizi yapılırken hata oluştu! Lütfen tekrar deneyin.');
    } finally {
      setIsLoadingAnalysis(false);
    }
  };

  useEffect(() => {
    loadStocks();
    loadMarketOverview();
    fetchMarketSentiment();
    fetchAlerts();
  }, []);

  // Renk yardımcı fonksiyonları
  const getChangeColor = (change: number) => {
    return change >= 0 ? 'text-green-400' : 'text-red-400';
  };

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'STRONG_BUY':
      case 'BUY':
        return 'bg-green-500/20 text-green-300 border border-green-400/30';
      case 'HOLD':
        return 'bg-yellow-500/20 text-yellow-300 border border-yellow-400/30';
      case 'SELL':
      case 'STRONG_SELL':
        return 'bg-red-500/20 text-red-300 border border-red-400/30';
      default:
        return 'bg-slate-500/20 text-slate-300 border border-slate-400/30';
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'LOW':
        return 'bg-green-500/20 text-green-300';
      case 'MEDIUM':
        return 'bg-yellow-500/20 text-yellow-300';
      case 'HIGH':
      case 'VERY_HIGH':
        return 'bg-red-500/20 text-red-300';
      default:
        return 'bg-slate-500/20 text-slate-300';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            📈 Borsa & Yatırım Asistanı
          </h1>
          <p className="text-slate-400 text-lg">
            AI destekli borsa analizi ve yatırım önerileri
          </p>
        </div>

        {/* Tab Navigation - Updated with new tabs */}
        <div className="flex flex-wrap gap-2 bg-slate-800/50 p-2 rounded-xl mb-8">
          {[
            { id: 'overview', label: '📊 Piyasa', icon: '📊' },
            { id: 'stocks', label: '💹 Hisseler', icon: '💹' },
            { id: 'ultra-analysis', label: '� Ultra Analiz', icon: '🚀' },
            { id: 'portfolio', label: '🎯 Portföy', icon: '🎯' },
            { id: 'sentiment', label: '📈 Sentiment', icon: '📈' },
            { id: 'screener', label: '🔍 Tarama', icon: '🔍' },
            { id: 'alerts', label: '🔔 Uyarılar', icon: '�' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex-1 min-w-[120px] px-4 py-3 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg transform scale-105'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <span className="text-lg">{tab.icon}</span>
              <div className="text-sm mt-1">{tab.label}</div>
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          
          {/* Piyasa Durumu Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {isLoadingOverview ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-4 border-green-500 border-t-transparent mx-auto mb-4"></div>
                  <p className="text-slate-300 text-lg">Piyasa verileri yükleniyor...</p>
                </div>
              ) : marketOverview ? (
                <>
                  {/* Ana Endeksler */}
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 backdrop-blur-sm rounded-2xl border border-blue-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">🏛️</div>
                        <div className="text-xs text-blue-300 bg-blue-500/20 px-2 py-1 rounded-full">BIST100</div>
                      </div>
                      <div className="text-2xl font-bold text-white mb-1">
                        {marketOverview.bist100?.value?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                      </div>
                      <div className={`text-sm ${getChangeColor(marketOverview.bist100?.change || 0)}`}>
                        {marketOverview.bist100?.change >= 0 ? '+' : ''}{marketOverview.bist100?.change?.toFixed(2) || '0.00'} 
                        ({marketOverview.bist100?.change_percent >= 0 ? '+' : ''}{marketOverview.bist100?.change_percent?.toFixed(2) || '0.00'}%)
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 backdrop-blur-sm rounded-2xl border border-yellow-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">💵</div>
                        <div className="text-xs text-yellow-300 bg-yellow-500/20 px-2 py-1 rounded-full">USD/TRY</div>
                      </div>
                      <div className="text-2xl font-bold text-white mb-1">
                        ₺{marketOverview.usd_try?.value?.toFixed(2) || 'N/A'}
                      </div>
                      <div className={`text-sm ${getChangeColor(marketOverview.usd_try?.change || 0)}`}>
                        {marketOverview.usd_try?.change >= 0 ? '+' : ''}{marketOverview.usd_try?.change?.toFixed(2) || '0.00'} 
                        ({marketOverview.usd_try?.change_percent >= 0 ? '+' : ''}{marketOverview.usd_try?.change_percent?.toFixed(2) || '0.00'}%)
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 backdrop-blur-sm rounded-2xl border border-purple-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">📈</div>
                        <div className="text-xs text-purple-300 bg-purple-500/20 px-2 py-1 rounded-full">GÜNÜN YILDIZI</div>
                      </div>
                      <div className="text-lg font-bold text-white mb-1">
                        {marketOverview.top_gainers?.[0]?.name || 'Veri yok'}
                      </div>
                      <div className={`text-sm ${getChangeColor(marketOverview.top_gainers?.[0]?.change_percent || 0)}`}>
                        +{marketOverview.top_gainers?.[0]?.change_percent?.toFixed(2) || '0.00'}%
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-emerald-500/20 to-emerald-600/20 backdrop-blur-sm rounded-2xl border border-emerald-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">🎯</div>
                        <div className="text-xs text-emerald-300 bg-emerald-500/20 px-2 py-1 rounded-full">ANALİZ</div>
                      </div>
                      <div className="text-lg font-bold text-white mb-1">
                        AI Önerisi
                      </div>
                      <div className="text-sm text-emerald-300">
                        {stocks.length} hisse analiz edildi
                      </div>
                    </div>
                  </div>

                  {/* En Çok Kazananlar ve Kaybedenler */}
                  <div className="grid lg:grid-cols-2 gap-6">
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                        📈 En Çok Kazananlar
                      </h3>
                      <div className="space-y-4">
                        {marketOverview.top_gainers.map((stock, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-green-500/10 rounded-xl border border-green-400/20">
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center text-green-300 font-bold">
                                {index + 1}
                              </div>
                              <div>
                                <div className="text-white font-medium">{stock.name}</div>
                                <div className="text-xs text-slate-400">{stock.symbol}</div>
                              </div>
                            </div>
                            <div className="text-green-300 font-semibold">
                              +{stock.change_percent.toFixed(2)}%
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                        📉 En Çok Kaybedenler
                      </h3>
                      <div className="space-y-4">
                        {marketOverview.top_losers.map((stock, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-red-500/10 rounded-xl border border-red-400/20">
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-red-500/20 rounded-lg flex items-center justify-center text-red-300 font-bold">
                                {index + 1}
                              </div>
                              <div>
                                <div className="text-white font-medium">{stock.name}</div>
                                <div className="text-xs text-slate-400">{stock.symbol}</div>
                              </div>
                            </div>
                            <div className="text-red-300 font-semibold">
                              {stock.change_percent.toFixed(2)}%
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">📊</div>
                  <p className="text-slate-300 text-lg">Piyasa verisi yüklenemedi</p>
                </div>
              )}
            </div>
          )}

          {/* Hisse Listesi Tab */}
          {activeTab === 'stocks' && (
            <div className="space-y-6">
              <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                <h3 className="text-xl font-semibold text-white mb-6">💹 BIST Hisseleri</h3>
                
                {isLoadingStocks ? (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-2 border-green-500 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-slate-300">Hisse verileri yükleniyor...</p>
                  </div>
                ) : (
                  <div className="grid gap-4">
                    {stocks.map((stock) => (
                      <div key={stock.symbol} className="bg-white/5 rounded-xl p-4 hover:bg-white/10 transition-all border border-white/10">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                              <span className="text-white font-bold text-sm">{stock.symbol.slice(0, 3)}</span>
                            </div>
                            <div>
                              <div className="text-white font-semibold">{stock.name}</div>
                              <div className="text-slate-400 text-sm">{stock.symbol} • {stock.sector}</div>
                            </div>
                          </div>
                          
                          <div className="text-right">
                            <div className="text-white text-xl font-bold">
                              ₺{stock.current_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                            </div>
                            <div className={`text-sm ${getChangeColor(stock.change_percent || 0)}`}>
                              {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent?.toFixed(2) || '0.00'}% 
                              ({stock.change_percent >= 0 ? '+' : ''}₺{stock.change_amount?.toFixed(2) || '0.00'})
                            </div>
                          </div>
                          
                          <div className="text-right">
                            <button
                              onClick={() => performUltraStockAnalysis(stock.symbol)}
                              disabled={isLoadingUltraAnalysis}
                              className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-3 py-2 rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed mr-2"
                            >
                              {isLoadingUltraAnalysis ? '🔄' : '🚀'}
                            </button>
                            <button
                              onClick={() => analyzeStock(stock.symbol)}
                              disabled={isLoadingAnalysis}
                              className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-4 py-2 rounded-lg hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed min-w-[100px] flex items-center justify-center"
                            >
                              {isLoadingAnalysis ? (
                                <>
                                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                                  Analiz...
                                </>
                              ) : (
                                '🔍 Analiz Et'
                              )}
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Hisse Analizi Tab */}
          {activeTab === 'analysis' && (
            <div className="space-y-6">
              {!stockAnalysis ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">🔍</div>
                  <p className="text-slate-300 text-lg">Hisse analizi için bir hisse seçin</p>
                  <p className="text-slate-400 text-sm mt-2">Hisse Listesi sekmesinden analiz etmek istediğiniz hisseyi seçebilirsiniz</p>
                </div>
              ) : (
                <>
                  {/* Analiz Başlığı */}
                  <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-4">
                        <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                          <span className="text-white font-bold">{stockAnalysis.symbol.slice(0, 3)}</span>
                        </div>
                        <div>
                          <h2 className="text-2xl font-bold text-white">{stockAnalysis.name}</h2>
                          <p className="text-slate-400">{stockAnalysis.symbol}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-white">
                          ₺{stockAnalysis.current_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                        </div>
                        <div className={`px-3 py-1 rounded-full text-sm font-medium ${getRecommendationColor(stockAnalysis.recommendation)}`}>
                          {stockAnalysis.recommendation_text}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Analiz Kartları */}
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h4 className="text-slate-300 font-medium mb-2">🎯 Hedef Fiyat</h4>
                      <div className="text-2xl font-bold text-green-400">
                        ₺{stockAnalysis.target_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        Potansiyel: +{(((stockAnalysis.target_price - stockAnalysis.current_price) / stockAnalysis.current_price) * 100).toFixed(1)}%
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h4 className="text-slate-300 font-medium mb-2">🛡️ Stop Loss</h4>
                      <div className="text-2xl font-bold text-red-400">
                        ₺{stockAnalysis.stop_loss_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        Risk: {stockAnalysis.current_price && stockAnalysis.stop_loss_price ? 
                          (((stockAnalysis.current_price - stockAnalysis.stop_loss_price) / stockAnalysis.current_price) * 100).toFixed(1) 
                          : '0'}%
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h4 className="text-slate-300 font-medium mb-2">⚖️ Risk Seviyesi</h4>
                      <div className={`text-lg font-semibold px-3 py-1 rounded-full ${getRiskColor(stockAnalysis.risk_level)}`}>
                        {stockAnalysis.risk_text}
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h4 className="text-slate-300 font-medium mb-2">🔢 Güven Skoru</h4>
                      <div className="text-2xl font-bold text-blue-400">
                        %{stockAnalysis.confidence_score.toFixed(1)}
                      </div>
                      <div className="w-full bg-slate-600 rounded-full h-2 mt-2">
                        <div 
                          className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-600"
                          style={{ width: `${stockAnalysis.confidence_score}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>

                  {/* Detaylı Analiz */}
                  <div className="grid lg:grid-cols-2 gap-6">
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4">🤖 AI Analizi</h3>
                      <p className="text-slate-200 leading-relaxed mb-4">
                        {stockAnalysis.analysis_text}
                      </p>
                      
                      <h4 className="text-white font-medium mb-3">🔑 Anahtar Faktörler:</h4>
                      <div className="space-y-2">
                        {stockAnalysis.key_factors.map((factor, index) => (
                          <div key={index} className="flex items-center space-x-2 text-slate-300">
                            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span>{factor}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4">📊 Teknik Göstergeler</h3>
                      
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                          <span className="text-slate-300">RSI</span>
                          <span className={`font-semibold ${
                            stockAnalysis.technical_indicators.rsi > 70 ? 'text-red-400' : 
                            stockAnalysis.technical_indicators.rsi < 30 ? 'text-green-400' : 'text-yellow-400'
                          }`}>
                            {stockAnalysis.technical_indicators.rsi.toFixed(1)}
                          </span>
                        </div>

                        <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                          <span className="text-slate-300">MACD Sinyali</span>
                          <span className={`px-2 py-1 rounded text-sm font-semibold ${
                            stockAnalysis.technical_indicators.macd_signal === 'BUY' ? 'bg-green-500/20 text-green-300' :
                            stockAnalysis.technical_indicators.macd_signal === 'SELL' ? 'bg-red-500/20 text-red-300' :
                            'bg-yellow-500/20 text-yellow-300'
                          }`}>
                            {stockAnalysis.technical_indicators.macd_signal}
                          </span>
                        </div>

                        <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                          <span className="text-slate-300">Trend</span>
                          <span className={`px-2 py-1 rounded text-sm font-semibold ${
                            stockAnalysis.technical_indicators.trend === 'BULLISH' ? 'bg-green-500/20 text-green-300' :
                            stockAnalysis.technical_indicators.trend === 'BEARISH' ? 'bg-red-500/20 text-red-300' :
                            'bg-yellow-500/20 text-yellow-300'
                          }`}>
                            {stockAnalysis.technical_indicators.trend}
                          </span>
                        </div>

                        <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                          <span className="text-slate-300">Haber Sentiment</span>
                          <span className={`px-2 py-1 rounded text-sm font-semibold ${
                            stockAnalysis.news_sentiment === 'POSITIVE' ? 'bg-green-500/20 text-green-300' :
                            stockAnalysis.news_sentiment === 'NEGATIVE' ? 'bg-red-500/20 text-red-300' :
                            'bg-yellow-500/20 text-yellow-300'
                          }`}>
                            {stockAnalysis.news_sentiment}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}

          {/* Ultra Advanced Stock Analysis Tab */}
          {activeTab === 'ultra-analysis' && (
            <div className="space-y-6">
              {!ultraAnalysis ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">🚀</div>
                  <h3 className="text-2xl font-bold text-white mb-4">Ultra Advanced Stock Analysis</h3>
                  <p className="text-slate-300 text-lg mb-6">AI-powered comprehensive stock analysis with advanced metrics</p>
                  
                  <div className="mb-6">
                    <select 
                      value={selectedStockForAnalysis}
                      onChange={(e) => setSelectedStockForAnalysis(e.target.value)}
                      className="bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none mr-4"
                    >
                      <option value="">Hisse Seçin</option>
                      {stocks.map(stock => (
                        <option key={stock.symbol} value={stock.symbol}>
                          {stock.name} ({stock.symbol})
                        </option>
                      ))}
                    </select>
                    
                    <button
                      onClick={() => selectedStockForAnalysis && performUltraStockAnalysis(selectedStockForAnalysis)}
                      disabled={!selectedStockForAnalysis || isLoadingUltraAnalysis}
                      className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-purple-600 hover:to-purple-700 transition-all transform hover:scale-105 font-medium disabled:opacity-50 disabled:transform-none"
                    >
                      {isLoadingUltraAnalysis ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent inline-block mr-2"></div>
                          Ultra Analiz Yapılıyor...
                        </>
                      ) : (
                        '🚀 Ultra Analiz Başlat'
                      )}
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Ultra Analysis Header */}
                  <div className="bg-gradient-to-r from-purple-500/20 to-purple-600/20 backdrop-blur-sm rounded-2xl border border-purple-400/30 p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h2 className="text-3xl font-bold text-white">{ultraAnalysis.symbol} Ultra Analysis</h2>
                        <p className="text-purple-300">AI-Powered Comprehensive Investment Analysis</p>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-white">
                          ₺{ultraAnalysis.current_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                        </div>
                        <div className={`px-4 py-2 rounded-full text-lg font-bold ${
                          ultraAnalysis.ai_analysis?.recommendation === 'STRONG_BUY' ? 'bg-green-500/20 text-green-300' :
                          ultraAnalysis.ai_analysis?.recommendation === 'BUY' ? 'bg-green-500/20 text-green-300' :
                          ultraAnalysis.ai_analysis?.recommendation === 'HOLD' ? 'bg-yellow-500/20 text-yellow-300' :
                          'bg-red-500/20 text-red-300'
                        }`}>
                          {ultraAnalysis.ai_analysis?.recommendation || 'N/A'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Key Metrics Cards */}
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-gradient-to-br from-green-500/20 to-emerald-600/20 backdrop-blur-sm rounded-2xl border border-green-400/30 p-6">
                      <div className="text-2xl mb-2">🎯</div>
                      <h4 className="text-green-300 font-medium mb-2">AI Güven Skoru</h4>
                      <div className="text-3xl font-bold text-white">
                        {ultraAnalysis.ai_analysis?.confidence_score || '0'}/100
                      </div>
                      <div className="w-full bg-slate-600 rounded-full h-2 mt-2">
                        <div 
                          className="h-2 rounded-full bg-gradient-to-r from-green-500 to-emerald-600"
                          style={{ width: `${ultraAnalysis.ai_analysis?.confidence_score || 0}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 backdrop-blur-sm rounded-2xl border border-blue-400/30 p-6">
                      <div className="text-2xl mb-2">📊</div>
                      <h4 className="text-blue-300 font-medium mb-2">Hedef Fiyat</h4>
                      <div className="text-3xl font-bold text-white">
                        ₺{ultraAnalysis.ai_analysis?.target_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                      </div>
                      <div className="text-sm text-blue-200 mt-1">
                        Potansiyel: {ultraAnalysis.ai_analysis?.target_price && ultraAnalysis.current_price ? 
                          (((ultraAnalysis.ai_analysis.target_price - ultraAnalysis.current_price) / ultraAnalysis.current_price) * 100).toFixed(1) 
                          : '0'}%
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-red-500/20 to-red-600/20 backdrop-blur-sm rounded-2xl border border-red-400/30 p-6">
                      <div className="text-2xl mb-2">⚡</div>
                      <h4 className="text-red-300 font-medium mb-2">Volatilite</h4>
                      <div className="text-3xl font-bold text-white">
                        {ultraAnalysis.risk_metrics?.volatility ? (ultraAnalysis.risk_metrics.volatility * 100).toFixed(1) : '0'}%
                      </div>
                      <div className="text-sm text-red-200 mt-1">
                        Risk: {ultraAnalysis.risk_metrics?.risk_category || 'Bilinmiyor'}
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 backdrop-blur-sm rounded-2xl border border-yellow-400/30 p-6">
                      <div className="text-2xl mb-2">📈</div>
                      <h4 className="text-yellow-300 font-medium mb-2">Sharpe Oranı</h4>
                      <div className="text-3xl font-bold text-white">
                        {ultraAnalysis.risk_metrics?.sharpe_ratio?.toFixed(2) || 'N/A'}
                      </div>
                      <div className="text-sm text-yellow-200 mt-1">
                        Risk-getiri dengesi
                      </div>
                    </div>
                  </div>

                  {/* AI Investment Thesis & Technical Analysis */}
                  <div className="grid lg:grid-cols-2 gap-6">
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                        🤖 AI Yatırım Tezi
                      </h3>
                      <p className="text-slate-200 leading-relaxed mb-6">
                        {ultraAnalysis.ai_analysis?.investment_thesis || 'Yatırım tezi henüz mevcut değil.'}
                      </p>
                      
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <h4 className="text-green-300 font-medium mb-3">✅ Artılar</h4>
                          <div className="space-y-2">
                            {ultraAnalysis.ai_insights?.pros?.map((pro, index) => (
                              <div key={index} className="text-sm text-slate-300 bg-green-500/10 p-2 rounded">
                                • {pro}
                              </div>
                            )) || <div className="text-sm text-slate-400">Henüz veri yok</div>}
                          </div>
                        </div>
                        
                        <div>
                          <h4 className="text-red-300 font-medium mb-3">❌ Eksiler</h4>
                          <div className="space-y-2">
                            {ultraAnalysis.ai_insights?.cons?.map((con, index) => (
                              <div key={index} className="text-sm text-slate-300 bg-red-500/10 p-2 rounded">
                                • {con}
                              </div>
                            )) || <div className="text-sm text-slate-400">Henüz veri yok</div>}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4">📊 Teknik Analiz</h3>
                      
                      <div className="space-y-4">
                        <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                          <span className="text-slate-300">RSI (14)</span>
                          <span className={`font-bold ${
                            ultraAnalysis.technical_analysis?.rsi > 70 ? 'text-red-400' : 
                            ultraAnalysis.technical_analysis?.rsi < 30 ? 'text-green-400' : 'text-yellow-400'
                          }`}>
                            {ultraAnalysis.technical_analysis?.rsi?.toFixed(1) || 'N/A'}
                          </span>
                        </div>

                        <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                          <span className="text-slate-300">Trend</span>
                          <span className={`px-2 py-1 rounded text-sm font-semibold ${
                            ultraAnalysis.technical_analysis?.trend_analysis?.includes('YUKSELİŞ') || ultraAnalysis.technical_analysis?.trend_analysis?.includes('BULLISH') ? 'bg-green-500/20 text-green-300' :
                            ultraAnalysis.technical_analysis?.trend_analysis?.includes('DÜŞÜŞ') || ultraAnalysis.technical_analysis?.trend_analysis?.includes('BEARISH') ? 'bg-red-500/20 text-red-300' :
                            'bg-yellow-500/20 text-yellow-300'
                          }`}>
                            {ultraAnalysis.technical_analysis?.trend_analysis || 'Bilinmiyor'}
                          </span>
                        </div>

                        <div className="p-3 bg-white/5 rounded-lg">
                          <div className="text-slate-300 mb-2">Destek Seviyeleri</div>
                          <div className="flex flex-wrap gap-2">
                            {ultraAnalysis.technical_analysis?.support_levels?.map((level, index) => (
                              <span key={index} className="px-2 py-1 bg-green-500/20 text-green-300 rounded text-sm">
                                ₺{level?.toFixed(2)}
                              </span>
                            )) || <span className="text-slate-400 text-sm">Henüz veri yok</span>}
                          </div>
                        </div>

                        <div className="p-3 bg-white/5 rounded-lg">
                          <div className="text-slate-300 mb-2">Direnç Seviyeleri</div>
                          <div className="flex flex-wrap gap-2">
                            {ultraAnalysis.technical_analysis?.resistance_levels?.map((level, index) => (
                              <span key={index} className="px-2 py-1 bg-red-500/20 text-red-300 rounded text-sm">
                                ₺{level?.toFixed(2)}
                              </span>
                            )) || <span className="text-slate-400 text-sm">Henüz veri yok</span>}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Risk & Catalysts */}
                  <div className="grid lg:grid-cols-2 gap-6">
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                        🚀 Katalizörler
                      </h3>
                      <div className="space-y-2">
                        {ultraAnalysis.ai_insights?.catalysts?.map((catalyst, index) => (
                          <div key={index} className="text-sm text-slate-300 bg-blue-500/10 p-2 rounded border-l-2 border-blue-400">
                            💡 {catalyst}
                          </div>
                        )) || <div className="text-sm text-slate-400">Henüz veri yok</div>}
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                        ⚠️ Risk Faktörleri
                      </h3>
                      <div className="space-y-2">
                        {ultraAnalysis.ai_insights?.risks?.map((risk, index) => (
                          <div key={index} className="text-sm text-slate-300 bg-red-500/10 p-2 rounded border-l-2 border-red-400">
                            ⚠️ {risk}
                          </div>
                        )) || <div className="text-sm text-slate-400">Henüz veri yok</div>}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Market Sentiment Tab */}
          {activeTab === 'sentiment' && (
            <div className="space-y-6">
              {!marketSentiment ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">📈</div>
                  <h3 className="text-2xl font-bold text-white mb-4">Market Sentiment Analysis</h3>
                  <p className="text-slate-300 text-lg mb-6">AI-powered real-time market sentiment and fear-greed analysis</p>
                  
                  <button
                    onClick={fetchMarketSentiment}
                    disabled={isLoadingSentiment}
                    className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all transform hover:scale-105 font-medium disabled:opacity-50 disabled:transform-none"
                  >
                    {isLoadingSentiment ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent inline-block mr-2"></div>
                        Sentiment Analizi...
                      </>
                    ) : (
                      '📈 Sentiment Analizi Yap'
                    )}
                  </button>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Overall Sentiment */}
                  <div className="bg-gradient-to-r from-blue-500/20 to-purple-600/20 backdrop-blur-sm rounded-2xl border border-blue-400/30 p-6">
                    <h2 className="text-2xl font-bold text-white mb-4">📊 Piyasa Genel Sentiment</h2>
                    <div className="grid md:grid-cols-3 gap-6">
                      <div className="text-center">
                        <div className={`text-6xl mb-2 ${
                          marketSentiment.overall_sentiment?.score > 0.6 ? 'text-green-400' :
                          marketSentiment.overall_sentiment?.score < 0.4 ? 'text-red-400' : 'text-yellow-400'
                        }`}>
                          {marketSentiment.overall_sentiment?.score > 0.6 ? '😄' :
                           marketSentiment.overall_sentiment?.score < 0.4 ? '😨' : '😐'}
                        </div>
                        <h3 className="text-lg font-semibold text-white">{marketSentiment.overall_sentiment?.label || 'N/A'}</h3>
                        <p className="text-slate-300">Skor: {marketSentiment.overall_sentiment?.score ? (marketSentiment.overall_sentiment.score * 100).toFixed(1) : '0'}/100</p>
                      </div>

                      <div className="text-center">
                        <div className="text-4xl mb-2">{
                          marketSentiment.fear_greed_index?.value > 75 ? '🤑' :
                          marketSentiment.fear_greed_index?.value > 50 ? '😊' :
                          marketSentiment.fear_greed_index?.value > 25 ? '😐' : '😱'
                        }</div>
                        <h3 className="text-lg font-semibold text-white">Fear & Greed Index</h3>
                        <p className="text-slate-300">{marketSentiment.fear_greed_index?.value || '0'}/100</p>
                        <p className={`text-sm font-medium ${
                          marketSentiment.fear_greed_index?.label === 'GREED' ? 'text-red-400' :
                          marketSentiment.fear_greed_index?.label === 'FEAR' ? 'text-blue-400' : 'text-yellow-400'
                        }`}>
                          {marketSentiment.fear_greed_index?.label || 'N/A'}
                        </p>
                      </div>

                      <div className="text-center">
                        <div className="text-4xl mb-2">📰</div>
                        <h3 className="text-lg font-semibold text-white">Haber Analizi</h3>
                        <p className="text-slate-300">{marketSentiment.news_analysis?.total_articles || '0'} makale</p>
                        <p className="text-green-400 text-sm">
                          Pozitif: %{marketSentiment.news_analysis?.positive_ratio ? (marketSentiment.news_analysis.positive_ratio * 100).toFixed(1) : '0'}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Sector Sentiments */}
                  <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                    <h3 className="text-xl font-semibold text-white mb-4">🏭 Sektörel Sentiment</h3>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {marketSentiment.sector_sentiments && Object.entries(marketSentiment.sector_sentiments).map(([sector, data]) => (
                        <div key={sector} className="bg-white/5 rounded-lg p-4">
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-white font-medium capitalize">{sector}</span>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              data.trend === 'RISING' || data.trend === 'YUKSELİŞ' ? 'bg-green-500/20 text-green-300' :
                              data.trend === 'FALLING' || data.trend === 'DÜŞÜŞ' ? 'bg-red-500/20 text-red-300' :
                              'bg-yellow-500/20 text-yellow-300'
                            }`}>
                              {data.trend === 'RISING' || data.trend === 'YUKSELİŞ' ? '📈' :
                               data.trend === 'FALLING' || data.trend === 'DÜŞÜŞ' ? '📉' : '➡️'}
                            </span>
                          </div>
                          <div className="w-full bg-slate-600 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                data.score > 0.6 ? 'bg-green-500' :
                                data.score < 0.4 ? 'bg-red-500' : 'bg-yellow-500'
                              }`}
                              style={{ width: `${(data.score || 0) * 100}%` }}
                            ></div>
                          </div>
                          <div className="text-xs text-slate-400 mt-1">
                            Skor: {((data.score || 0) * 100).toFixed(1)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Portfolio Optimization Tab */}
          {activeTab === 'portfolio' && (
            <div className="space-y-6">
              {!portfolioOptimization ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">🎯</div>
                  <h3 className="text-2xl font-bold text-white mb-4">AI Portfolio Optimizer</h3>
                  <p className="text-slate-300 text-lg mb-6">Modern Portföy Teorisi ile optimal portföy dağılımı</p>
                  
                  <button
                    onClick={optimizePortfolio}
                    disabled={isLoadingPortfolio}
                    className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all transform hover:scale-105 font-medium disabled:opacity-50 disabled:transform-none"
                  >
                    {isLoadingPortfolio ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent inline-block mr-2"></div>
                        Portföy Optimize Ediliyor...
                      </>
                    ) : (
                      '🎯 Portföy Optimizasyonu Yap'
                    )}
                  </button>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Portfolio Header */}
                  <div className="bg-gradient-to-r from-blue-500/20 to-blue-600/20 backdrop-blur-sm rounded-2xl border border-blue-400/30 p-6">
                    <h2 className="text-2xl font-bold text-white mb-2">🎯 Optimize Edilmiş Portföy</h2>
                    <p className="text-blue-300">Modern Portföy Teorisi ile hesaplanmış optimal dağılım</p>
                  </div>

                  {/* Key Metrics */}
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-gradient-to-br from-green-500/20 to-emerald-600/20 backdrop-blur-sm rounded-2xl border border-green-400/30 p-6">
                      <div className="text-2xl mb-2">📈</div>
                      <h4 className="text-green-300 font-medium mb-2">Beklenen Getiri</h4>
                      <div className="text-3xl font-bold text-white">
                        %{portfolioOptimization.expected_return ? (portfolioOptimization.expected_return * 100).toFixed(1) : '0.0'}
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-red-500/20 to-red-600/20 backdrop-blur-sm rounded-2xl border border-red-400/30 p-6">
                      <div className="text-2xl mb-2">⚡</div>
                      <h4 className="text-red-300 font-medium mb-2">Beklenen Risk</h4>
                      <div className="text-3xl font-bold text-white">
                        %{portfolioOptimization.expected_risk ? (portfolioOptimization.expected_risk * 100).toFixed(1) : '0.0'}
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 backdrop-blur-sm rounded-2xl border border-yellow-400/30 p-6">
                      <div className="text-2xl mb-2">📊</div>
                      <h4 className="text-yellow-300 font-medium mb-2">Sharpe Oranı</h4>
                      <div className="text-3xl font-bold text-white">
                        {portfolioOptimization.sharpe_ratio?.toFixed(2) || 'N/A'}
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 backdrop-blur-sm rounded-2xl border border-purple-400/30 p-6">
                      <div className="text-2xl mb-2">🎯</div>
                      <h4 className="text-purple-300 font-medium mb-2">Risk Skoru</h4>
                      <div className="text-3xl font-bold text-white">
                        {portfolioOptimization.risk_score?.toFixed(1) || 'N/A'}/10
                      </div>
                    </div>
                  </div>

                  {/* Portfolio Allocation */}
                  <div className="grid lg:grid-cols-2 gap-6">
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4">💼 Optimal Dağılım</h3>
                      <div className="space-y-4">
                        {portfolioOptimization.optimized_allocation && Object.entries(portfolioOptimization.optimized_allocation).map(([symbol, weight]) => (
                          <div key={symbol} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                            <span className="text-white font-medium">{symbol}</span>
                            <div className="flex items-center space-x-3">
                              <div className="w-32 bg-slate-600 rounded-full h-2">
                                <div 
                                  className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-600"
                                  style={{ width: `${weight * 100}%` }}
                                ></div>
                              </div>
                              <span className="text-blue-300 font-semibold min-w-[50px]">
                                %{(weight * 100).toFixed(1)}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                      <h3 className="text-xl font-semibold text-white mb-4">🏢 Sektör Dağılımı</h3>
                      <div className="space-y-3">
                        {portfolioOptimization.diversification_analysis?.sector_distribution && Object.entries(portfolioOptimization.diversification_analysis.sector_distribution).map(([sector, weight]) => (
                          <div key={sector} className="flex items-center justify-between">
                            <span className="text-slate-300">{sector}</span>
                            <span className="text-white font-semibold">%{(weight * 100).toFixed(1)}</span>
                          </div>
                        ))}
                      </div>
                      
                      <div className="mt-6 p-3 bg-green-500/10 rounded-lg">
                        <h4 className="text-green-300 font-medium mb-2">📊 Diversifikasyon Analizi</h4>
                        <p className="text-slate-300 text-sm">
                          Konsantrasyon Riski: <span className="text-green-400 font-medium">{portfolioOptimization.diversification_analysis?.concentration_risk}</span>
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Stock Screener Tab */}
          {activeTab === 'screener' && (
            <div className="space-y-6">
              {!stockScreener ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">🔍</div>
                  <h3 className="text-2xl font-bold text-white mb-4">AI Stock Screener</h3>
                  <p className="text-slate-300 text-lg mb-6">Personalized stock recommendations based on advanced AI analysis</p>
                  
                  <button
                    onClick={performStockScreening}
                    disabled={isLoadingScreener}
                    className="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-green-700 transition-all transform hover:scale-105 font-medium disabled:opacity-50 disabled:transform-none"
                  >
                    {isLoadingScreener ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent inline-block mr-2"></div>
                        Hisse Taranıyor...
                      </>
                    ) : (
                      '🔍 Hisse Taraması Yap'
                    )}
                  </button>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Screener Header */}
                  <div className="bg-gradient-to-r from-green-500/20 to-green-600/20 backdrop-blur-sm rounded-2xl border border-green-400/30 p-6">
                    <h2 className="text-2xl font-bold text-white mb-2">🎯 AI Hisse Önerileri</h2>
                    <p className="text-green-300">{stockScreener.total_found} hisse analiz edildi, en iyileri seçildi</p>
                  </div>

                  {/* Stock Recommendations */}
                  <div className="grid gap-6">
                    {stockScreener.recommendations.map((stock, index) => (
                      <div key={stock.symbol} className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6 hover:border-green-400/30 transition-all">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center space-x-4">
                            <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
                              <span className="text-white font-bold">{index + 1}</span>
                            </div>
                            <div>
                              <h3 className="text-xl font-bold text-white">{stock.name}</h3>
                              <p className="text-slate-400">{stock.symbol}</p>
                              <div className="flex items-center space-x-3 mt-2">
                                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                                  stock.recommendation === 'STRONG_BUY' ? 'bg-green-500/20 text-green-300' :
                                  stock.recommendation === 'BUY' ? 'bg-green-500/20 text-green-300' :
                                  'bg-yellow-500/20 text-yellow-300'
                                }`}>
                                  {stock.recommendation}
                                </span>
                                <span className="text-white font-bold">
                                  AI Skor: {stock.ai_score}/100
                                </span>
                              </div>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-2xl font-bold text-white">
                              ₺{stock.current_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                            </div>
                            <div className="text-green-400 text-sm">
                              Hedef: ₺{stock.target_price?.toLocaleString('tr-TR', { minimumFractionDigits: 2 }) || 'N/A'}
                            </div>
                            <div className="text-blue-400 text-sm">
                              Potansiyel: +{stock.upside_potential?.toFixed(1) || '0.0'}%
                            </div>
                          </div>
                        </div>

                        <p className="text-slate-200 mb-4 leading-relaxed">
                          {stock.investment_thesis}
                        </p>

                        <div className="grid md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="text-green-300 font-medium mb-2">Anahtar Faktörler:</h4>
                            <div className="space-y-1">
                              {stock.key_factors.map((factor, i) => (
                                <div key={i} className="text-sm text-slate-300 flex items-center">
                                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                                  {factor}
                                </div>
                              ))}
                            </div>
                          </div>
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-slate-400 text-sm">Risk Seviyesi</p>
                              <span className={`px-2 py-1 rounded text-sm font-medium ${
                                stock.risk_level === 'LOW' ? 'bg-green-500/20 text-green-300' :
                                stock.risk_level === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-300' :
                                'bg-red-500/20 text-red-300'
                              }`}>
                                {stock.risk_level}
                              </span>
                            </div>
                            <div className="text-right">
                              <p className="text-slate-400 text-sm">Önerilen Ağırlık</p>
                              <p className="text-white font-bold">%{stock.suggested_allocation ? (stock.suggested_allocation * 100).toFixed(1) : '0.0'}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Alerts Tab */}
          {activeTab === 'alerts' && (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-red-500/20 to-red-600/20 backdrop-blur-sm rounded-2xl border border-red-400/30 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-2xl font-bold text-white mb-2">🔔 Gerçek Zamanlı Uyarılar</h2>
                    <p className="text-red-300">AI-powered market alerts and notifications</p>
                  </div>
                  <button
                    onClick={fetchAlerts}
                    disabled={isLoadingAlerts}
                    className="bg-gradient-to-r from-red-500 to-red-600 text-white px-4 py-2 rounded-xl hover:from-red-600 hover:to-red-700 transition-all font-medium disabled:opacity-50"
                  >
                    {isLoadingAlerts ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent inline-block mr-2"></div>
                        Yenileniyor...
                      </>
                    ) : (
                      '🔄 Yenile'
                    )}
                  </button>
                </div>
              </div>

              {!alerts ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">🔔</div>
                  <p className="text-slate-300 text-lg">Uyarılar yükleniyor...</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {alerts.alerts.length === 0 ? (
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                      <div className="text-6xl mb-4">✅</div>
                      <h3 className="text-xl font-bold text-white mb-2">Aktif Uyarı Yok</h3>
                      <p className="text-slate-400">Şu anda herhangi bir uyarı bulunmuyor.</p>
                    </div>
                  ) : (
                    alerts.alerts.map((alert, index) => (
                      <div key={alert.id} className={`bg-slate-800/30 backdrop-blur-sm rounded-2xl border p-6 ${
                        alert.priority === 'HIGH' ? 'border-red-400/30 bg-red-500/5' :
                        alert.priority === 'MEDIUM' ? 'border-yellow-400/30 bg-yellow-500/5' :
                        'border-blue-400/30 bg-blue-500/5'
                      }`}>
                        <div className="flex items-start justify-between">
                          <div className="flex items-center space-x-4">
                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                              alert.type === 'PRICE_ALERT' ? 'bg-green-500/20 text-green-400' :
                              alert.type === 'TECHNICAL_SIGNAL' ? 'bg-blue-500/20 text-blue-400' :
                              alert.type === 'NEWS_ALERT' ? 'bg-purple-500/20 text-purple-400' :
                              'bg-red-500/20 text-red-400'
                            }`}>
                              {alert.type === 'PRICE_ALERT' ? '💰' :
                               alert.type === 'TECHNICAL_SIGNAL' ? '📊' :
                               alert.type === 'NEWS_ALERT' ? '📰' : '⚠️'}
                            </div>
                            <div>
                              <div className="flex items-center space-x-2 mb-1">
                                <h3 className="text-white font-semibold">{alert.symbol}</h3>
                                <span className={`px-2 py-1 rounded text-xs font-medium ${
                                  alert.priority === 'HIGH' ? 'bg-red-500/20 text-red-300' :
                                  alert.priority === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-300' :
                                  'bg-blue-500/20 text-blue-300'
                                }`}>
                                  {alert.priority}
                                </span>
                                {alert.is_active && (
                                  <span className="px-2 py-1 bg-green-500/20 text-green-300 rounded text-xs">
                                    AKTİF
                                  </span>
                                )}
                              </div>
                              <p className="text-slate-300">{alert.message}</p>
                              <p className="text-slate-400 text-sm mt-1">
                                {new Date(alert.created_at).toLocaleDateString('tr-TR', {
                                  year: 'numeric',
                                  month: 'short',
                                  day: 'numeric',
                                  hour: '2-digit',
                                  minute: '2-digit'
                                })}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default StockMarketDashboard;
