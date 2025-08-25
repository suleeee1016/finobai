import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

interface FinancialGoal {
  id: number;
  name: string;
  description: string;
  category: string;
  category_display: string;
  target_amount: number;
  current_amount: number;
  target_date: string;
  priority: number;
  priority_display: string;
  status: string;
  status_display: string;
  progress_percentage: number;
  remaining_amount: number;
  is_completed: boolean;
  months_remaining: number;
  created_at: string;
}

interface GoalContribution {
  id: number;
  amount: number;
  source: string;
  note: string;
  date: string;
}

interface DashboardSummary {
  total_goals: number;
  completed_goals: number;
  active_goals: number;
  total_target_amount: number;
  total_saved_amount: number;
  overall_progress: number;
  monthly_contribution_total: number;
  goals_by_category: { [key: string]: { count: number; total_target: number; total_saved: number } };
  upcoming_deadlines: Array<{
    goal_name: string;
    target_date: string;
    days_remaining: number;
    progress: number;
  }>;
}

const FinancialGoalsDashboard: React.FC = () => {
  const { user, token } = useAuth();
  
  // State hooks - always at the top
  const [activeGoalsTab, setActiveGoalsTab] = useState<'overview' | 'goals' | 'create'>('overview');
  const [goals, setGoals] = useState<FinancialGoal[]>([]);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [aiRecommendations, setAiRecommendations] = useState<any>(null);
  const [personalAnalysis, setPersonalAnalysis] = useState<any>(null);
  const [selectedGoal, setSelectedGoal] = useState<FinancialGoal | null>(null);

  // Form states
  const [newGoal, setNewGoal] = useState({
    name: '',
    description: '',
    category: 'custom',
    target_amount: '',
    target_date: '',
    monthly_contribution: '',
    priority: 2
  });

  const [newContribution, setNewContribution] = useState({
    amount: '',
    source: 'manual',
    note: ''
  });

  // Categories data
  const categories = [
    { value: 'house', label: '🏠 Ev Almak', color: '#10B981' },
    { value: 'car', label: '🚗 Araç Almak', color: '#3B82F6' },
    { value: 'vacation', label: '🌴 Tatil/Seyahat', color: '#F59E0B' },
    { value: 'wedding', label: '💍 Düğün', color: '#EC4899' },
    { value: 'education', label: '🎓 Eğitim', color: '#8B5CF6' },
    { value: 'emergency', label: '🚨 Acil Durum Fonu', color: '#EF4444' },
    { value: 'retirement', label: '💰 Emeklilik', color: '#6B7280' },
    { value: 'health', label: '🏥 Sağlık', color: '#059669' },
    { value: 'investment', label: '💼 Yatırım', color: '#DC2626' },
    { value: 'custom', label: '⭐ Özel Hedef', color: '#7C3AED' },
  ];

  // All React hooks must be called before any early return
  const fetchDashboardSummary = useCallback(async () => {
    try {
      setLoading(true);
      if (!token || !user) {
        console.error('Token veya kullanıcı bulunamadı');
        alert('Oturum süresi dolmuş. Lütfen tekrar giriş yapın.');
        return;
      }
      
      const response = await axios.get('http://localhost:8000/api/goals/goals/dashboard_summary/', {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setSummary(response.data);
    } catch (error) {
      console.error('Dashboard summary alınamadı:', error);
      if (error.response?.status === 403) {
        alert('Yetkisiz erişim. Lütfen tekrar giriş yapın.');
      }
    } finally {
      setLoading(false);
    }
  }, [token, user]);

  const fetchGoals = useCallback(async () => {
    try {
      setLoading(true);
      if (!token || !user) {
        console.error('Token veya kullanıcı bulunamadı');
        alert('Oturum süresi dolmuş. Lütfen tekrar giriş yapın.');
        return;
      }
      
      const response = await axios.get('http://localhost:8000/api/goals/goals/', {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setGoals(response.data);
    } catch (error) {
      console.error('Hedefler alınamadı:', error);
      if (error.response?.status === 403) {
        alert('Yetkisiz erişim. Lütfen tekrar giriş yapın.');
      }
    } finally {
      setLoading(false);
    }
  }, [token, user]);

  const fetchAIRecommendations = useCallback(async () => {
    try {
      setLoading(true);
      if (!token || !user) {
        console.error('Token veya kullanıcı bulunamadı');
        return;
      }
      
      const response = await axios.get('http://localhost:8000/api/goals/recommendations/', {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setAiRecommendations(response.data);
    } catch (error) {
      console.error('AI önerileri alınamadı:', error);
    } finally {
      setLoading(false);
    }
  }, [token, user]);

  const fetchPersonalAnalysis = useCallback(async () => {
    try {
      setLoading(true);
      if (!token || !user) {
        console.error('Token veya kullanıcı bulunamadı');
        return;
      }
      
      const response = await axios.get('http://localhost:8000/api/goals/personal-analysis/', {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setPersonalAnalysis(response.data);
    } catch (error) {
      console.error('Kişisel analiz alınamadı:', error);
    } finally {
      setLoading(false);
    }
  }, [token, user]);

  useEffect(() => {
    if (activeGoalsTab === 'overview') {
      fetchDashboardSummary();
    } else if (activeGoalsTab === 'goals') {
      fetchGoals();
    }
  }, [activeGoalsTab, fetchDashboardSummary, fetchGoals]);

  // Render login screen if not authenticated
  if (!user || !token) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20 text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-red-500/20 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.99-.833-2.76 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-white mb-4">🔐 Giriş Gerekli</h2>
            <p className="text-slate-300 mb-6">
              Finansal hedeflerinizi görüntülemek için giriş yapmanız gerekiyor.
            </p>
            <button
              onClick={() => window.location.href = '/login'}
              className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-green-600 hover:to-emerald-700 transition-all"
            >
              Giriş Yap
            </button>
          </div>
        </div>
      </div>
    );
  }

  const createGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (!token || !user) {
        console.error('Token veya kullanıcı bulunamadı');
        alert('Oturum süresi dolmuş. Lütfen tekrar giriş yapın.');
        return;
      }
      
      const goalData = {
        ...newGoal,
        target_amount: parseFloat(newGoal.target_amount),
        monthly_contribution: parseFloat(newGoal.monthly_contribution)
      };

      await axios.post('http://localhost:8000/api/goals/goals/', goalData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      // Form'u temizle
      setNewGoal({
        name: '',
        description: '',
        category: 'custom',
        target_amount: '',
        target_date: '',
        monthly_contribution: '',
        priority: 2
      });
      setShowCreateModal(false);
      
      // Hedefleri yeniden yükle
      fetchGoals();
      fetchDashboardSummary();
      
    } catch (error) {
      console.error('Hedef oluşturulamadı:', error);
      alert('Hedef oluşturulamadı. Lütfen bilgilerinizi kontrol edin.');
    } finally {
      setLoading(false);
    }
  };

  const addContribution = async (goalId: number) => {
    try {
      setLoading(true);
      if (!token || !user) {
        console.error('Token veya kullanıcı bulunamadı');
        alert('Oturum süresi dolmuş. Lütfen tekrar giriş yapın.');
        return;
      }
      
      const contributionData = {
        goal: goalId,
        amount: parseFloat(newContribution.amount),
        source: newContribution.source,
        note: newContribution.note
      };

      await axios.post(`http://localhost:8000/api/goals/goals/${goalId}/add_contribution/`, contributionData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      // Form'u temizle
      setNewContribution({
        amount: '',
        source: 'manual',
        note: ''
      });
      
      // Hedefleri yeniden yükle
      fetchGoals();
      fetchDashboardSummary();
      
    } catch (error) {
      console.error('Katkı eklenemedi:', error);
      alert('Katkı eklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (category: string) => {
    const cat = categories.find(c => c.value === category);
    return cat ? cat.label.split(' ')[0] : '⭐';
  };

  const getCategoryColor = (category: string) => {
    const cat = categories.find(c => c.value === category);
    return cat ? cat.color : '#7C3AED';
  };

  const formatCurrency = (amount: number) => {
    return `₺${amount.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('tr-TR');
  };

  const getPriorityColor = (priority: number) => {
    switch (priority) {
      case 1: return 'text-red-400 bg-red-500/20';
      case 2: return 'text-yellow-400 bg-yellow-500/20';
      case 3: return 'text-green-400 bg-green-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-blue-400 bg-blue-500/20';
      case 'completed': return 'text-green-400 bg-green-500/20';
      case 'paused': return 'text-yellow-400 bg-yellow-500/20';
      case 'cancelled': return 'text-red-400 bg-red-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-6 border border-white/20">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">🎯 Finansal Hedefler</h1>
            <p className="text-slate-300">Hedeflerinizi belirleyin, takip edin ve gerçekleştirin</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all transform hover:scale-105 font-medium"
          >
            ➕ Yeni Hedef Ekle
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="backdrop-blur-xl bg-white/10 rounded-2xl border border-white/20">
        <div className="flex border-b border-white/10">
          <button
            onClick={() => setActiveGoalsTab('overview')}
            className={`px-6 py-4 text-sm font-medium transition-all ${
              activeGoalsTab === 'overview'
                ? 'text-green-300 border-b-2 border-green-400 bg-green-500/10'
                : 'text-slate-300 hover:text-white'
            }`}
          >
            📊 Genel Bakış
          </button>
          <button
            onClick={() => setActiveGoalsTab('goals')}
            className={`px-6 py-4 text-sm font-medium transition-all ${
              activeGoalsTab === 'goals'
                ? 'text-green-300 border-b-2 border-green-400 bg-green-500/10'
                : 'text-slate-300 hover:text-white'
            }`}
          >
            🎯 Hedeflerim
          </button>
          <button
            onClick={() => {
              setActiveGoalsTab('create');
              fetchAIRecommendations();
            }}
            className={`px-6 py-4 text-sm font-medium transition-all ${
              activeGoalsTab === 'create'
                ? 'text-green-300 border-b-2 border-green-400 bg-green-500/10'
                : 'text-slate-300 hover:text-white'
            }`}
          >
            🤖 AI Önerileri
          </button>
        </div>

        <div className="p-6">
          {loading && (
            <div className="flex justify-center items-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-400"></div>
            </div>
          )}

          {/* Overview Tab */}
          {activeGoalsTab === 'overview' && summary && !loading && (
            <div className="space-y-6">
              {/* Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="backdrop-blur-xl bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-xl p-6 border border-blue-400/30">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-white">Toplam Hedef</h3>
                    <span className="text-2xl">🎯</span>
                  </div>
                  <p className="text-3xl font-bold text-blue-300">{summary.total_goals}</p>
                  <p className="text-sm text-blue-200 mt-2">
                    {summary.active_goals} aktif, {summary.completed_goals} tamamlandı
                  </p>
                </div>

                <div className="backdrop-blur-xl bg-gradient-to-br from-green-500/20 to-emerald-600/20 rounded-xl p-6 border border-green-400/30">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-white">Toplam Hedef Tutar</h3>
                    <span className="text-2xl">💰</span>
                  </div>
                  <p className="text-3xl font-bold text-green-300">
                    {formatCurrency(summary.total_target_amount)}
                  </p>
                  <p className="text-sm text-green-200 mt-2">Tüm hedefler toplamı</p>
                </div>

                <div className="backdrop-blur-xl bg-gradient-to-br from-purple-500/20 to-purple-600/20 rounded-xl p-6 border border-purple-400/30">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-white">Biriken Tutar</h3>
                    <span className="text-2xl">📈</span>
                  </div>
                  <p className="text-3xl font-bold text-purple-300">
                    {formatCurrency(summary.total_saved_amount)}
                  </p>
                  <p className="text-sm text-purple-200 mt-2">
                    %{summary.overall_progress.toFixed(1)} tamamlandı
                  </p>
                </div>

                <div className="backdrop-blur-xl bg-gradient-to-br from-orange-500/20 to-orange-600/20 rounded-xl p-6 border border-orange-400/30">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-white">Aylık Katkı</h3>
                    <span className="text-2xl">📅</span>
                  </div>
                  <p className="text-3xl font-bold text-orange-300">
                    {formatCurrency(summary.monthly_contribution_total)}
                  </p>
                  <p className="text-sm text-orange-200 mt-2">Planlanan toplam</p>
                </div>
              </div>

              {/* Progress Overview */}
              <div className="backdrop-blur-xl bg-white/5 rounded-xl p-6 border border-white/10">
                <h3 className="text-xl font-semibold text-white mb-6">Genel İlerleme</h3>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">Toplam İlerleme</span>
                    <span className="text-white">{summary.overall_progress.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-3">
                    <div 
                      className="bg-gradient-to-r from-green-400 to-emerald-500 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(summary.overall_progress, 100)}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Category Breakdown */}
              <div className="backdrop-blur-xl bg-white/5 rounded-xl p-6 border border-white/10">
                <h3 className="text-xl font-semibold text-white mb-6">Kategori Dağılımı</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(summary.goals_by_category).map(([category, data]) => (
                    <div key={category} className="bg-white/5 rounded-lg p-4 border border-white/10">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-white font-medium">{category}</span>
                        <span className="text-slate-400 text-sm">{data.count} hedef</span>
                      </div>
                      <p className="text-sm text-green-400">{formatCurrency(data.total_saved)}</p>
                      <p className="text-xs text-slate-400">/ {formatCurrency(data.total_target)}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Upcoming Deadlines */}
              {summary.upcoming_deadlines.length > 0 && (
                <div className="backdrop-blur-xl bg-red-500/10 rounded-xl p-6 border border-red-400/30">
                  <h3 className="text-xl font-semibold text-white mb-6">⚠️ Yaklaşan Deadline'lar</h3>
                  <div className="space-y-3">
                    {summary.upcoming_deadlines.map((deadline, index) => (
                      <div key={index} className="bg-white/5 rounded-lg p-4 border border-red-400/20">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="text-white font-medium">{deadline.goal_name}</p>
                            <p className="text-sm text-slate-400">
                              {formatDate(deadline.target_date)} - {deadline.days_remaining} gün kaldı
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-red-300">%{deadline.progress.toFixed(1)}</p>
                            <p className="text-xs text-slate-400">tamamlandı</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Goals Tab */}
          {activeGoalsTab === 'goals' && !loading && (
            <div className="space-y-6">
              {goals.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">🎯</div>
                  <h3 className="text-xl font-semibold text-white mb-2">Henüz hedef belirlenmemiş</h3>
                  <p className="text-slate-400 mb-6">İlk finansal hedefinizi oluşturun ve takip etmeye başlayın</p>
                  <button
                    onClick={() => setShowCreateModal(true)}
                    className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all transform hover:scale-105 font-medium"
                  >
                    İlk Hedefinizi Oluşturun
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {goals.map((goal) => (
                    <div key={goal.id} className="backdrop-blur-xl bg-white/5 rounded-xl p-6 border border-white/10 hover:border-white/20 transition-all">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div 
                            className="w-12 h-12 rounded-lg flex items-center justify-center text-2xl"
                            style={{ backgroundColor: `${getCategoryColor(goal.category)}20` }}
                          >
                            {getCategoryIcon(goal.category)}
                          </div>
                          <div>
                            <h4 className="text-lg font-semibold text-white">{goal.name}</h4>
                            <p className="text-sm text-slate-400">{goal.category_display}</p>
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <span className={`px-2 py-1 rounded-lg text-xs font-medium ${getPriorityColor(goal.priority)}`}>
                            {goal.priority_display}
                          </span>
                          <span className={`px-2 py-1 rounded-lg text-xs font-medium ${getStatusColor(goal.status)}`}>
                            {goal.status_display}
                          </span>
                        </div>
                      </div>

                      {goal.description && (
                        <p className="text-slate-300 text-sm mb-4">{goal.description}</p>
                      )}

                      <div className="space-y-4">
                        {/* Progress */}
                        <div>
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-sm text-slate-300">İlerleme</span>
                            <span className="text-sm font-medium text-white">
                              {formatCurrency(goal.current_amount)} / {formatCurrency(goal.target_amount)}
                            </span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500"
                              style={{ width: `${Math.min(goal.progress_percentage, 100)}%` }}
                            />
                          </div>
                          <div className="flex justify-between items-center mt-1">
                            <span className="text-xs text-slate-400">%{goal.progress_percentage.toFixed(1)} tamamlandı</span>
                            <span className="text-xs text-slate-400">{goal.months_remaining} ay kaldı</span>
                          </div>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-2 gap-4">
                          <div className="text-center">
                            <p className="text-xs text-slate-400">Kalan Tutar</p>
                            <p className="text-sm font-medium text-white">{formatCurrency(goal.remaining_amount)}</p>
                          </div>
                          <div className="text-center">
                            <p className="text-xs text-slate-400">Hedef Tarihi</p>
                            <p className="text-sm font-medium text-white">{formatDate(goal.target_date)}</p>
                          </div>
                        </div>

                        {/* Add Contribution */}
                        <div className="border-t border-white/10 pt-4">
                          <div className="flex space-x-2">
                            <input
                              type="number"
                              placeholder="Katkı tutarı"
                              value={selectedGoal?.id === goal.id ? newContribution.amount : ''}
                              onChange={(e) => {
                                setSelectedGoal(goal);
                                setNewContribution(prev => ({ ...prev, amount: e.target.value }));
                              }}
                              className="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:border-green-400 focus:outline-none"
                            />
                            <button
                              onClick={() => selectedGoal?.id === goal.id && addContribution(goal.id)}
                              disabled={!newContribution.amount || selectedGoal?.id !== goal.id}
                              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all"
                            >
                              Ekle
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* AI Recommendations Tab */}
          {activeGoalsTab === 'create' && (
            <div className="space-y-6">
              {/* Tab Selection */}
              <div className="flex space-x-4 bg-white/5 rounded-xl p-2 border border-white/10">
                <button
                  onClick={() => {
                    setAiRecommendations(null);
                    setPersonalAnalysis(null);
                  }}
                  className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all ${
                    !aiRecommendations && !personalAnalysis
                      ? 'bg-green-500 text-white shadow-lg'
                      : 'text-slate-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  🤖 Genel Öneriler
                </button>
                <button
                  onClick={() => {
                    setAiRecommendations(null);
                    setPersonalAnalysis(null);
                  }}
                  className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all ${
                    personalAnalysis
                      ? 'bg-purple-500 text-white shadow-lg'
                      : 'text-slate-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  🎯 Kişisel Analiz
                </button>
              </div>

              {/* Content Based on Selection */}
              {!aiRecommendations && !personalAnalysis ? (
                <div className="grid md:grid-cols-2 gap-6">
                  {/* General Recommendations */}
                  <div className="text-center py-12 backdrop-blur-xl bg-white/5 rounded-xl border border-white/10">
                    <div className="text-6xl mb-4">🤖</div>
                    <h3 className="text-xl font-semibold text-white mb-2">Genel AI Önerileri</h3>
                    <p className="text-slate-400 mb-6">Genel hedef ve strateji önerilerini alın</p>
                    <button
                      onClick={fetchAIRecommendations}
                      className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all transform hover:scale-105 font-medium"
                    >
                      Genel Öneriler Al
                    </button>
                  </div>

                  {/* Personal Analysis */}
                  <div className="text-center py-12 backdrop-blur-xl bg-white/5 rounded-xl border border-white/10">
                    <div className="text-6xl mb-4">🎯</div>
                    <h3 className="text-xl font-semibold text-white mb-2">Kişisel Finansal Analiz</h3>
                    <p className="text-slate-400 mb-6">Size özel detaylı analiz ve stratejiler</p>
                    <button
                      onClick={fetchPersonalAnalysis}
                      className="bg-gradient-to-r from-purple-500 to-violet-600 text-white px-6 py-3 rounded-xl hover:from-purple-600 hover:to-violet-700 transition-all transform hover:scale-105 font-medium"
                    >
                      Kişisel Analiz Al
                    </button>
                  </div>
                </div>
              ) : aiRecommendations ? (
                <div className="backdrop-blur-xl bg-white/5 rounded-xl p-6 border border-white/10">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-white">🎯 Kişiselleştirilmiş Hedef Önerileri</h3>
                    <button
                      onClick={() => setAiRecommendations(null)}
                      className="text-slate-400 hover:text-white transition-colors"
                    >
                      ✕ Kapat
                    </button>
                  </div>
                  {aiRecommendations.success ? (
                    <div className="space-y-6">
                      {aiRecommendations.recommendations?.new_goal_suggestions?.map((suggestion: any, index: number) => (
                        <div key={index} className="bg-white/5 rounded-lg p-4 border border-white/10">
                          <div className="flex justify-between items-start mb-3">
                            <div>
                              <h4 className="text-white font-medium">{getCategoryIcon(suggestion.category)} {suggestion.name}</h4>
                              <p className="text-sm text-slate-400">Önerilen Tutar: {formatCurrency(suggestion.estimated_amount)}</p>
                            </div>
                            <span className={`px-2 py-1 rounded-lg text-xs font-medium ${
                              suggestion.priority === 'yüksek' ? 'bg-red-500/20 text-red-400' :
                              suggestion.priority === 'orta' ? 'bg-yellow-500/20 text-yellow-400' :
                              'bg-green-500/20 text-green-400'
                            }`}>
                              {suggestion.priority}
                            </span>
                          </div>
                          <button
                            onClick={() => {
                              setNewGoal(prev => ({
                                ...prev,
                                name: suggestion.name,
                                category: suggestion.category,
                                target_amount: suggestion.estimated_amount.toString(),
                                priority: suggestion.priority === 'yüksek' ? 1 : suggestion.priority === 'orta' ? 2 : 3
                              }));
                              setShowCreateModal(true);
                            }}
                            className="text-sm bg-green-500/20 text-green-400 px-3 py-1 rounded-lg hover:bg-green-500/30 transition-all"
                          >
                            Hedef Olarak Ekle
                          </button>
                        </div>
                      ))}
                      
                      <div className="bg-blue-500/10 rounded-lg p-4 border border-blue-400/20">
                        <h4 className="text-white font-medium mb-2">💡 İyileştirme Önerileri</h4>
                        <ul className="space-y-1">
                          {aiRecommendations.recommendations?.improvement_suggestions?.map((tip: string, index: number) => (
                            <li key={index} className="text-sm text-slate-300">• {tip}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <p className="text-red-400">AI önerileri alınamadı. Lütfen tekrar deneyin.</p>
                    </div>
                  )}
                </div>
              ) : personalAnalysis ? (
                <div className="backdrop-blur-xl bg-white/5 rounded-xl p-6 border border-white/10">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-white">🎯 Kişisel Finansal Analiz</h3>
                    <button
                      onClick={() => setPersonalAnalysis(null)}
                      className="text-slate-400 hover:text-white transition-colors"
                    >
                      ✕ Kapat
                    </button>
                  </div>
                  {personalAnalysis.success ? (
                    <div className="space-y-6">
                      {/* Kişisel Durum Özeti */}
                      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-lg p-6 border border-blue-400/20">
                        <h4 className="text-white font-medium mb-4">📊 Finansal Sağlık Durumunuz</h4>
                        <div className="grid md:grid-cols-4 gap-4 mb-4">
                          <div className="text-center p-3 bg-white/5 rounded-lg">
                            <div className={`text-3xl mb-2 ${
                              personalAnalysis.analysis.kisisel_durum?.finansal_saglik_skoru >= 80 ? 'text-green-400' :
                              personalAnalysis.analysis.kisisel_durum?.finansal_saglik_skoru >= 60 ? 'text-yellow-400' :
                              'text-red-400'
                            }`}>
                              {personalAnalysis.analysis.kisisel_durum?.finansal_saglik_skoru >= 80 ? '🌟' :
                               personalAnalysis.analysis.kisisel_durum?.finansal_saglik_skoru >= 60 ? '⚠️' : '❗'}
                            </div>
                            <p className="text-xs text-slate-400">Finansal Sağlık Skoru</p>
                            <p className="text-lg font-bold text-white">{personalAnalysis.analysis.kisisel_durum?.finansal_saglik_skoru}/100</p>
                          </div>
                          <div className="text-center p-3 bg-white/5 rounded-lg">
                            <div className="text-2xl mb-2">🎯</div>
                            <p className="text-xs text-slate-400">Hedef Stratejisi</p>
                            <p className="text-sm font-medium text-white capitalize">{personalAnalysis.analysis.kisisel_durum?.hedef_stratejisi}</p>
                          </div>
                          <div className="text-center p-3 bg-white/5 rounded-lg">
                            <div className="text-2xl mb-2">💰</div>
                            <p className="text-xs text-slate-400">Tasarruf Kapasitesi</p>
                            <p className="text-sm font-medium text-white capitalize">{personalAnalysis.analysis.kisisel_durum?.tasarruf_kapasitesi}</p>
                          </div>
                          <div className="text-center p-3 bg-white/5 rounded-lg">
                            <div className="text-2xl mb-2">📈</div>
                            <p className="text-xs text-slate-400">Risk Profili</p>
                            <p className="text-sm font-medium text-white capitalize">{personalAnalysis.analysis.kisisel_durum?.risk_profili}</p>
                          </div>
                        </div>
                        <div className="bg-white/5 rounded-lg p-4">
                          <p className="text-slate-300 text-sm leading-relaxed">{personalAnalysis.analysis.kisisel_durum?.genel_degerlendirme}</p>
                        </div>
                      </div>

                      {/* Hedef Analizi */}
                      <div className="bg-green-500/10 rounded-lg p-6 border border-green-400/20">
                        <h4 className="text-white font-medium mb-4">🎯 Hedef Stratejisi Analizi</h4>
                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <h5 className="text-green-300 font-medium mb-2">Öncelik Sıralaması</h5>
                            <div className="space-y-2">
                              {personalAnalysis.analysis.hedef_analizi?.hedef_siralama_onerisi?.map((hedef: string, index: number) => (
                                <div key={index} className="flex items-center space-x-3 p-2 bg-white/5 rounded">
                                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                                    index === 0 ? 'bg-red-500 text-white' :
                                    index === 1 ? 'bg-yellow-500 text-black' :
                                    'bg-green-500 text-white'
                                  }`}>
                                    {index + 1}
                                  </span>
                                  <span className="text-white text-sm">{hedef}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                          <div>
                            <h5 className="text-green-300 font-medium mb-2">Gerçekçi Timeline</h5>
                            <div className="bg-white/5 rounded-lg p-3">
                              <p className="text-white text-sm">{personalAnalysis.analysis.hedef_analizi?.gecersiz_timeline}</p>
                            </div>
                            <h5 className="text-green-300 font-medium mb-2 mt-4">İlk Odaklanılacak</h5>
                            <div className="bg-white/5 rounded-lg p-3">
                              <p className="text-white text-sm font-medium">{personalAnalysis.analysis.hedef_analizi?.ilk_odaklanilmasi_gereken}</p>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Harcama Optimizasyonu */}
                      <div className="bg-orange-500/10 rounded-lg p-6 border border-orange-400/20">
                        <h4 className="text-white font-medium mb-4">💡 Harcama Optimizasyonu</h4>
                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <h5 className="text-orange-300 font-medium mb-3">Tasarruf Fırsatları</h5>
                            <div className="space-y-3">
                              {personalAnalysis.analysis.harcama_optimizasyonu?.kesinti_yapilabilir_kategoriler?.map((item: any, index: number) => (
                                <div key={index} className="bg-white/5 rounded-lg p-3">
                                  <div className="flex justify-between items-center mb-2">
                                    <span className="text-white font-medium capitalize">{item.kategori}</span>
                                    <span className="text-green-400 font-bold">₺{item.tasarruf}</span>
                                  </div>
                                  <div className="text-xs text-slate-400">
                                    Mevcut: ₺{item.mevcut} → Hedef: ₺{item.hedef}
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                          <div>
                            <h5 className="text-orange-300 font-medium mb-3">Aylık Tasarruf Potansiyeli</h5>
                            <div className="bg-white/5 rounded-lg p-4 text-center">
                              <div className="text-3xl font-bold text-green-400 mb-2">
                                ₺{personalAnalysis.analysis.harcama_optimizasyonu?.aylık_tasarruf_potansiyeli}
                              </div>
                              <p className="text-xs text-slate-400">Aylık tasarruf hedefi</p>
                            </div>
                            {personalAnalysis.analysis.harcama_optimizasyonu?.kritik_harcamalar && (
                              <div className="mt-4">
                                <h5 className="text-orange-300 font-medium mb-2">Dikkat Edilmesi Gerekenler</h5>
                                <div className="space-y-1">
                                  {personalAnalysis.analysis.harcama_optimizasyonu.kritik_harcamalar.map((kategori: string, index: number) => (
                                    <div key={index} className="text-sm text-red-300 bg-red-500/10 px-2 py-1 rounded">
                                      ⚠️ {kategori}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Aylık Eylem Planı */}
                      <div className="bg-purple-500/10 rounded-lg p-6 border border-purple-400/20">
                        <h4 className="text-white font-medium mb-4">📅 3 Aylık Eylem Planı</h4>
                        <div className="grid gap-4">
                          {personalAnalysis.analysis.eylem_plani?.slice(0, 3).map((plan: any, index: number) => (
                            <div key={index} className="bg-white/5 rounded-lg p-4">
                              <div className="flex items-center justify-between mb-3">
                                <h5 className="text-purple-300 font-medium">{plan.ay}. Ay</h5>
                                <span className="text-xs bg-purple-500/20 text-purple-300 px-2 py-1 rounded">{plan.odak}</span>
                              </div>
                              <div className="grid md:grid-cols-2 gap-4">
                                <div>
                                  <p className="text-xs text-slate-400 mb-2">Hedef Katkıları:</p>
                                  {plan.hedefler?.map((hedef: string, i: number) => (
                                    <p key={i} className="text-sm text-white">• {hedef}</p>
                                  ))}
                                </div>
                                <div>
                                  <p className="text-xs text-slate-400 mb-2">Harcama Hedefleri:</p>
                                  {Object.entries(plan.harcama_hedefleri || {}).map(([kat, limit]: [string, any], i: number) => (
                                    <p key={i} className="text-sm text-white">• {kat}: ₺{limit}</p>
                                  ))}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Motivasyon ve Uyarılar */}
                      <div className="grid md:grid-cols-2 gap-4">
                        <div className="bg-green-500/10 rounded-lg p-4 border border-green-400/20">
                          <h4 className="text-white font-medium mb-3">� Motivasyon Önerileri</h4>
                          <div className="space-y-2">
                            {personalAnalysis.analysis.motivasyon_onerileri?.map((oneri: string, index: number) => (
                              <div key={index} className="text-sm text-slate-300 bg-white/5 p-2 rounded">
                                🌟 {oneri}
                              </div>
                            ))}
                          </div>
                        </div>
                        <div className="bg-red-500/10 rounded-lg p-4 border border-red-400/20">
                          <h4 className="text-white font-medium mb-3">⚠️ Risk Uyarıları</h4>
                          <div className="space-y-2">
                            {personalAnalysis.analysis.risk_uyarilari?.map((uyari: string, index: number) => (
                              <div key={index} className="text-sm text-slate-300 bg-white/5 p-2 rounded">
                                ⚠️ {uyari}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <p className="text-red-400">Kişisel analiz alınamadı. Lütfen tekrar deneyin.</p>
                    </div>
                  )}
                </div>
              ) : null}
            </div>
          )}
        </div>
      </div>

      {/* Create Goal Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="backdrop-blur-xl bg-slate-800/90 rounded-2xl p-6 w-full max-w-2xl border border-slate-700 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-white">🎯 Yeni Finansal Hedef</h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-slate-400 hover:text-white transition-all"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form onSubmit={createGoal} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Hedef Adı</label>
                  <input
                    type="text"
                    required
                    value={newGoal.name}
                    onChange={(e) => setNewGoal(prev => ({ ...prev, name: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none"
                    placeholder="Örn: Yeni Araba"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Kategori</label>
                  <select
                    value={newGoal.category}
                    onChange={(e) => setNewGoal(prev => ({ ...prev, category: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none"
                  >
                    {categories.map(cat => (
                      <option key={cat.value} value={cat.value}>{cat.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Açıklama (Opsiyonel)</label>
                <textarea
                  value={newGoal.description}
                  onChange={(e) => setNewGoal(prev => ({ ...prev, description: e.target.value }))}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none"
                  rows={3}
                  placeholder="Hedefiniz hakkında detay..."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Hedef Tutar (₺)</label>
                  <input
                    type="number"
                    required
                    min="0"
                    step="0.01"
                    value={newGoal.target_amount}
                    onChange={(e) => setNewGoal(prev => ({ ...prev, target_amount: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none"
                    placeholder="100000"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Hedef Tarihi</label>
                  <input
                    type="date"
                    required
                    value={newGoal.target_date}
                    min={new Date().toISOString().split('T')[0]}
                    onChange={(e) => setNewGoal(prev => ({ ...prev, target_date: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Aylık Katkı (₺)</label>
                  <input
                    type="number"
                    required
                    min="0"
                    step="0.01"
                    value={newGoal.monthly_contribution}
                    onChange={(e) => setNewGoal(prev => ({ ...prev, monthly_contribution: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none"
                    placeholder="1000"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Öncelik</label>
                  <select
                    value={newGoal.priority}
                    onChange={(e) => setNewGoal(prev => ({ ...prev, priority: parseInt(e.target.value) }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:border-green-400 focus:outline-none"
                  >
                    <option value={1}>🔴 Yüksek</option>
                    <option value={2}>🟡 Orta</option>
                    <option value={3}>🟢 Düşük</option>
                  </select>
                </div>
              </div>

              <div className="flex space-x-4 pt-6 border-t border-slate-700">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 bg-slate-600 hover:bg-slate-500 text-white px-6 py-3 rounded-xl font-medium transition-all"
                >
                  İptal
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all font-medium disabled:opacity-50"
                >
                  {loading ? 'Oluşturuluyor...' : 'Hedef Oluştur'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FinancialGoalsDashboard;
