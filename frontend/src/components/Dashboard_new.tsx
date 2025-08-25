import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext.tsx';
import { useNavigate, Link } from 'react-router-dom';
import ChatBot from './ChatBot/ChatBot.tsx';
import ExpenseAnalysisDashboard from './ExpenseAnalysisDashboard.tsx';
import StockMarketDashboard from './StockMarketDashboard.tsx';
import FinancialGoalsDashboard from './FinancialGoalsDashboard.tsx';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'dashboard' | 'expenses' | 'stocks' | 'goals' | 'chatbot'>('dashboard');
  const [isChatBotOpen, setIsChatBotOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  // Mock data - gerçek API'den gelecek
  const mockData = {
    balance: 45678.90,
    monthlyIncome: 12500,
    monthlyExpense: 8750,
    savings: 36928.90,
    investments: 15250,
    monthlyGrowth: 8.5,
    recentTransactions: [
      { id: 1, type: 'gelir', description: 'Maaş', amount: 12500, date: '2025-08-20' },
      { id: 2, type: 'gider', description: 'Market Alışverişi', amount: -285.50, date: '2025-08-19' },
      { id: 3, type: 'gider', description: 'Elektrik Faturası', amount: -150.00, date: '2025-08-18' },
      { id: 4, type: 'gelir', description: 'Yatırım Getirisi', amount: 450.00, date: '2025-08-17' },
      { id: 5, type: 'gider', description: 'Su Faturası', amount: -85.25, date: '2025-08-16' },
    ],
    portfolioData: [
      { name: 'BTC', value: 45250, change: 2.5 },
      { name: 'ETH', value: 28500, change: -1.2 },
      { name: 'BIST100', value: 15250, change: 3.8 },
      { name: 'USD/TRY', value: 28.45, change: -0.5 },
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-900">
      {/* Header */}
      <header className="backdrop-blur-xl bg-white/10 border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-4">
              <Link to="/" className="flex items-center">
                <img src="/images/finobaai.png" alt="Finobai" className="h-10" />
              </Link>
              <nav className="hidden md:flex space-x-8">
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activeTab === 'dashboard'
                      ? 'bg-green-500/20 text-green-300 border border-green-400/30'
                      : 'text-slate-300 hover:text-white hover:bg-white/5'
                  }`}
                >
                  📊 Ana Sayfa
                </button>
                <button
                  onClick={() => setActiveTab('expenses')}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activeTab === 'expenses'
                      ? 'bg-green-500/20 text-green-300 border border-green-400/30'
                      : 'text-slate-300 hover:text-white hover:bg-white/5'
                  }`}
                >
                  💳 Harcama Analizi
                </button>
                <button
                  onClick={() => setActiveTab('stocks')}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activeTab === 'stocks'
                      ? 'bg-green-500/20 text-green-300 border border-green-400/30'
                      : 'text-slate-300 hover:text-white hover:bg-white/5'
                  }`}
                >
                  📈 Borsa & Yatırım
                </button>
                <button
                  onClick={() => setActiveTab('goals')}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activeTab === 'goals'
                      ? 'bg-green-500/20 text-green-300 border border-green-400/30'
                      : 'text-slate-300 hover:text-white hover:bg-white/5'
                  }`}
                >
                  🎯 Finansal Hedefler
                </button>
                <button
                  onClick={() => setActiveTab('chatbot')}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activeTab === 'chatbot'
                      ? 'bg-green-500/20 text-green-300 border border-green-400/30'
                      : 'text-slate-300 hover:text-white hover:bg-white/5'
                  }`}
                >
                  🤖 AI Asistan
                </button>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right hidden sm:block">
                <p className="text-sm text-slate-300">Hoş geldiniz,</p>
                <p className="text-sm font-medium text-white">
                  {user?.first_name} {user?.last_name}
                </p>
              </div>
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-emerald-500 flex items-center justify-center">
                <span className="text-white font-semibold text-sm">
                  {user?.first_name?.[0]}{user?.last_name?.[0]}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="bg-red-500/20 hover:bg-red-500/30 text-red-300 hover:text-red-200 px-4 py-2 rounded-lg text-sm font-medium transition-all border border-red-400/30"
              >
                Çıkış Yap
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            {/* Welcome Banner */}
            <div className="backdrop-blur-xl bg-gradient-to-r from-green-500/20 to-emerald-600/20 rounded-2xl p-6 border border-green-400/30">
              <h1 className="text-3xl font-bold text-white mb-2">
                Hoş geldiniz, {user?.first_name}! 👋
              </h1>
              <p className="text-slate-300">
                Finansal durumunuzu kontrol altında tutun ve hedeflerinize ulaşın.
              </p>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-medium text-slate-300">Toplam Bakiye</h3>
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <svg className="w-5 h-5 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                    </svg>
                  </div>
                </div>
                <p className="text-3xl font-bold text-white">
                  ₺{mockData.balance.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}
                </p>
                <p className="text-sm text-green-400 mt-2">
                  +{mockData.monthlyGrowth}% bu ay
                </p>
              </div>

              <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-medium text-slate-300">Aylık Gelir</h3>
                  <div className="p-2 bg-green-500/20 rounded-lg">
                    <svg className="w-5 h-5 text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                  </div>
                </div>
                <p className="text-3xl font-bold text-white">
                  ₺{mockData.monthlyIncome.toLocaleString('tr-TR')}
                </p>
                <p className="text-sm text-slate-400 mt-2">
                  Bu ay toplam
                </p>
              </div>

              <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-medium text-slate-300">Aylık Gider</h3>
                  <div className="p-2 bg-red-500/20 rounded-lg">
                    <svg className="w-5 h-5 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                    </svg>
                  </div>
                </div>
                <p className="text-3xl font-bold text-white">
                  ₺{mockData.monthlyExpense.toLocaleString('tr-TR')}
                </p>
                <p className="text-sm text-slate-400 mt-2">
                  Bu ay toplam
                </p>
              </div>

              <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-medium text-slate-300">Toplam Tasarruf</h3>
                  <div className="p-2 bg-purple-500/20 rounded-lg">
                    <svg className="w-5 h-5 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                    </svg>
                  </div>
                </div>
                <p className="text-3xl font-bold text-white">
                  ₺{mockData.savings.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}
                </p>
                <p className="text-sm text-slate-400 mt-2">
                  Hedefte %78
                </p>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-6">Son İşlemler</h3>
                <div className="space-y-4">
                  {mockData.recentTransactions.slice(0, 5).map((transaction) => (
                    <div key={transaction.id} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                          transaction.type === 'gelir' ? 'bg-green-500/20' : 'bg-red-500/20'
                        }`}>
                          {transaction.type === 'gelir' ? (
                            <svg className="w-5 h-5 text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                            </svg>
                          ) : (
                            <svg className="w-5 h-5 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
                            </svg>
                          )}
                        </div>
                        <div>
                          <p className="text-white font-medium">{transaction.description}</p>
                          <p className="text-xs text-slate-400">{new Date(transaction.date).toLocaleDateString('tr-TR')}</p>
                        </div>
                      </div>
                      <span className={`font-semibold ${
                        transaction.amount > 0 ? 'text-green-300' : 'text-red-300'
                      }`}>
                        {transaction.amount > 0 ? '+' : ''}₺{Math.abs(transaction.amount).toLocaleString('tr-TR', { minimumFractionDigits: 2 })}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-6">Hızlı Aksiyonlar</h3>
                <div className="space-y-4">
                  <button 
                    onClick={() => setActiveTab('goals')}
                    className="w-full p-4 bg-gradient-to-r from-purple-500/20 to-violet-600/20 hover:from-purple-500/30 hover:to-violet-600/30 rounded-xl border border-purple-400/30 text-left transition-all"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                        <span className="text-2xl">🎯</span>
                      </div>
                      <div>
                        <p className="text-white font-medium">Finansal Hedefler</p>
                        <p className="text-sm text-slate-400">Hedeflerinizi takip edin</p>
                      </div>
                    </div>
                  </button>

                  <button 
                    onClick={() => setActiveTab('expenses')}
                    className="w-full p-4 bg-gradient-to-r from-blue-500/20 to-indigo-600/20 hover:from-blue-500/30 hover:to-indigo-600/30 rounded-xl border border-blue-400/30 text-left transition-all"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                        <svg className="w-5 h-5 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                      </div>
                      <div>
                        <p className="text-white font-medium">Harcama Analizi</p>
                        <p className="text-sm text-slate-400">AI destekli analiz</p>
                      </div>
                    </div>
                  </button>

                  <button 
                    onClick={() => setActiveTab('stocks')}
                    className="w-full p-4 bg-gradient-to-r from-green-500/20 to-emerald-600/20 hover:from-green-500/30 hover:to-emerald-600/30 rounded-xl border border-green-400/30 text-left transition-all"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                        <span className="text-2xl">📈</span>
                      </div>
                      <div>
                        <p className="text-white font-medium">Borsa & Yatırım</p>
                        <p className="text-sm text-slate-400">Hisse analizi</p>
                      </div>
                    </div>
                  </button>

                  <button 
                    onClick={() => setIsChatBotOpen(true)}
                    className="w-full p-4 bg-gradient-to-r from-yellow-500/20 to-orange-600/20 hover:from-yellow-500/30 hover:to-orange-600/30 rounded-xl border border-yellow-400/30 text-left transition-all"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                        <svg className="w-5 h-5 text-yellow-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                      </div>
                      <div>
                        <p className="text-white font-medium">AI Tavsiyesi</p>
                        <p className="text-sm text-slate-400">Kişiselleştirilmiş öneriler</p>
                      </div>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'expenses' && (
          <div className="relative">
            <ExpenseAnalysisDashboard />
          </div>
        )}

        {activeTab === 'stocks' && (
          <div className="relative">
            <StockMarketDashboard />
          </div>
        )}

        {activeTab === 'goals' && (
          <div className="relative">
            <FinancialGoalsDashboard />
          </div>
        )}

        {activeTab === 'chatbot' && (
          <div className="space-y-6">
            <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20 text-center">
              <h2 className="text-2xl font-bold text-white mb-4">🤖 AI Finans Asistanı</h2>
              <p className="text-slate-300 mb-6">
                Sağ alt köşedeki chat butonuna tıklayarak AI asistanınızla konuşmaya başlayabilirsiniz.
              </p>
              <button
                onClick={() => setIsChatBotOpen(true)}
                className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all transform hover:scale-105 font-medium"
              >
                💬 Chat Başlat
              </button>
            </div>
          </div>
        )}
      </main>

      {/* AI ChatBot */}
      <ChatBot 
        isOpen={isChatBotOpen} 
        onToggle={() => setIsChatBotOpen(!isChatBotOpen)} 
      />
    </div>
  );
};

export default Dashboard;
