import React, { useState, useEffect } from 'react';

interface ExpenseData {
  amount: number;
  description: string;
  category?: string;
  date: string;
}

interface AnalysisResult {
  category: string;
  confidence: number;
  is_necessary: boolean;
  tags: string[];
  analysis: string;
  category_info: {
    name: string;
    icon: string;
    color: string;
  };
}

interface MonthlyData {
  total_spent: number;
  expense_count: number;
  category_summary: any;
  insights: any[];
  average_per_day: number;
  top_category?: string;
}

interface CreditCardAnalysis {
  summary: {
    total_amount: number;
    transaction_count: number;
    avg_transaction: number;
    date_range: {
      start: string;
      end: string;
    };
  };
  category_analysis: any;
  top_categories: Array<{
    category: string;
    name: string;
    icon: string;
    amount: number;
    percentage: number;
  }>;
  insights: Array<{
    type: string;
    icon: string;
    title: string;
    message: string;
    priority: number;
    amount: number;
  }>;
  categorized_transactions: Array<{
    date: string;
    description: string;
    amount: number;
    category: string;
    confidence: number;
  }>;
}

const ExpenseAnalysisDashboard: React.FC = () => {
  const [expenseData, setExpenseData] = useState<ExpenseData>({
    amount: 0,
    description: '',
    date: new Date().toISOString().split('T')[0]
  });
  
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [monthlyData, setMonthlyData] = useState<MonthlyData | null>(null);
  const [creditCardAnalysis, setCreditCardAnalysis] = useState<CreditCardAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isLoadingMonthly, setIsLoadingMonthly] = useState(false);
  const [isUploadingStatement, setIsUploadingStatement] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [statementList, setStatementList] = useState<any[]>([]);
  const [selectedStatement, setSelectedStatement] = useState<any>(null);
  const [isLoadingStatements, setIsLoadingStatements] = useState(false);
  const [activeTab, setActiveTab] = useState<'analyze' | 'summary' | 'upload' | 'insights' | 'history'>('analyze');

  // Harcama analizi yap
  const analyzeExpense = async () => {
    if (!expenseData.amount || !expenseData.description) {
      alert('Lütfen tutar ve açıklama giriniz!');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await fetch('http://localhost:8001/api/expenses/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          expense_text: expenseData.description,
          amount: expenseData.amount
        })
      });

      if (!response.ok) throw new Error('Analiz başarısız');

      const data = await response.json();
      setAnalysisResult(data.analysis);
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Harcama analizi yapılırken hata oluştu!');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Aylık özet getir
  const loadMonthlySummary = async () => {
    setIsLoadingMonthly(true);
    try {
      const response = await fetch('http://localhost:8001/api/expenses/summary/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Özet alınamadı');

      const data = await response.json();
      setMonthlyData(data);
    } catch (error) {
      console.error('Monthly summary error:', error);
      alert('Aylık özet alınırken hata oluştu!');
    } finally {
      setIsLoadingMonthly(false);
    }
  };

  // Kredi kartı ekstresi yükle ve analiz et
  const uploadCreditCardStatement = async () => {
    if (!selectedFile) {
      alert('Lütfen bir ekstre dosyası seçiniz!');
      return;
    }

    setIsUploadingStatement(true);
    setCreditCardAnalysis(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8001/api/expenses/upload-statement/', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Ekstre yükleme başarısız');
      }

      const data = await response.json();
      setCreditCardAnalysis(data.analysis);
      alert(`✅ ${data.transaction_count} işlem başarıyla analiz edildi!`);
      
    } catch (error: any) {
      console.error('Statement upload error:', error);
      alert(`Ekstre analizi hatası: ${error.message}`);
    } finally {
      setIsUploadingStatement(false);
    }
  };

  // Dosya seçme
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Dosya tipi kontrolü
      const validTypes = ['.csv', '.txt', '.xlsx'];
      const isValidType = validTypes.some(type => file.name.toLowerCase().endsWith(type));
      
      if (!isValidType) {
        alert('Sadece CSV, TXT veya XLSX dosyaları destekleniyor!');
        return;
      }
      
      // Dosya boyutu kontrolü (5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('Dosya boyutu 5MB\'dan küçük olmalı!');
        return;
      }
      
      setSelectedFile(file);
    }
  };

  // Ekstreleri listele
  const loadStatements = async () => {
    setIsLoadingStatements(true);
    try {
      const response = await fetch('http://localhost:8001/api/expenses/statements/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Ekstreler alınamadı');

      const data = await response.json();
      setStatementList(data.statements);
    } catch (error) {
      console.error('Statement list error:', error);
      alert('Ekstre listesi alınırken hata oluştu!');
    } finally {
      setIsLoadingStatements(false);
    }
  };

  // Ekstre detayını getir
  const loadStatementDetail = async (statementId: number) => {
    try {
      const response = await fetch(`http://localhost:8001/api/expenses/statements/${statementId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Ekstre detayı alınamadı');

      const data = await response.json();
      setSelectedStatement(data);
    } catch (error) {
      console.error('Statement detail error:', error);
      alert('Ekstre detayı alınırken hata oluştu!');
    }
  };

  // useEffect - Tab değişikliklerini izle
  useEffect(() => {
    if (activeTab === 'summary' && !monthlyData) {
      loadMonthlySummary();
    }
    if (activeTab === 'history') {
      loadStatements();
    }
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            💳 Harcama Analizi Dashboard
          </h1>
          <p className="text-slate-400 text-lg">
            AI destekli finansal analiz ve içgörüler
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-xl mb-8">
          {[
            { id: 'analyze', label: '🔍 Harcama Analizi', icon: '🔍' },
            { id: 'upload', label: '📄 Ekstre Analizi', icon: '📄' },
            { id: 'summary', label: '📊 Aylık Özet', icon: '📊' },
            { id: 'insights', label: '💡 İçgörüler', icon: '💡' },
            { id: 'history', label: '📋 Ekstre Geçmişi', icon: '📋' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex-1 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          
          {/* Harcama Analizi Tab */}
          {activeTab === 'analyze' && (
            <div className="grid lg:grid-cols-2 gap-8">
              
              {/* Input Form */}
              <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                <h2 className="text-2xl font-semibold text-white mb-6 flex items-center">
                  📝 Harcama Bilgileri
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-slate-300 mb-2 font-medium">💰 Tutar (₺)</label>
                    <input
                      type="number"
                      value={expenseData.amount || ''}
                      onChange={(e) => setExpenseData(prev => ({
                        ...prev,
                        amount: parseFloat(e.target.value) || 0
                      }))}
                      className="w-full bg-slate-700/50 text-white rounded-xl px-4 py-3 border border-slate-600 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500/20"
                      placeholder="0.00"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-300 mb-2 font-medium">📋 Açıklama</label>
                    <input
                      type="text"
                      value={expenseData.description}
                      onChange={(e) => setExpenseData(prev => ({
                        ...prev,
                        description: e.target.value
                      }))}
                      className="w-full bg-slate-700/50 text-white rounded-xl px-4 py-3 border border-slate-600 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500/20"
                      placeholder="Örn: Migros market alışverişi"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-300 mb-2 font-medium">📅 Tarih</label>
                    <input
                      type="date"
                      value={expenseData.date}
                      onChange={(e) => setExpenseData(prev => ({
                        ...prev,
                        date: e.target.value
                      }))}
                      className="w-full bg-slate-700/50 text-white rounded-xl px-4 py-3 border border-slate-600 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500/20"
                    />
                  </div>

                  <button
                    onClick={analyzeExpense}
                    disabled={isAnalyzing || !expenseData.amount || !expenseData.description}
                    className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold py-3 rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                        Analiz Ediliyor...
                      </>
                    ) : (
                      <>🔍 Harcamayı Analiz Et</>
                    )}
                  </button>
                </div>
              </div>

              {/* Analysis Results */}
              <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                <h2 className="text-2xl font-semibold text-white mb-6 flex items-center">
                  🎯 Analiz Sonuçları
                </h2>
                
                {analysisResult ? (
                  <div className="space-y-4">
                    {/* Kategori */}
                    <div className="bg-slate-700/30 rounded-xl p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-300 font-medium">Kategori</span>
                        <span className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded-full">
                          %{(analysisResult.confidence * 100).toFixed(0)} güven
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">{analysisResult.category_info.icon}</span>
                        <span className="text-white font-semibold">{analysisResult.category_info.name}</span>
                      </div>
                    </div>

                    {/* Gereklilik */}
                    <div className="bg-slate-700/30 rounded-xl p-4">
                      <span className="text-slate-300 font-medium block mb-2">Gereklilik Durumu</span>
                      <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                        analysisResult.is_necessary 
                          ? 'bg-blue-500/20 text-blue-300 border border-blue-400/30' 
                          : 'bg-yellow-500/20 text-yellow-300 border border-yellow-400/30'
                      }`}>
                        {analysisResult.is_necessary ? '✅ Gerekli Harcama' : '⚠️ İsteğe Bağlı'}
                      </div>
                    </div>

                    {/* Etiketler */}
                    {analysisResult.tags.length > 0 && (
                      <div className="bg-slate-700/30 rounded-xl p-4">
                        <span className="text-slate-300 font-medium block mb-2">Etiketler</span>
                        <div className="flex flex-wrap gap-2">
                          {analysisResult.tags.map((tag, index) => (
                            <span key={index} className="bg-purple-500/20 text-purple-300 px-2 py-1 rounded-lg text-xs border border-purple-400/30">
                              #{tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* AI Analizi */}
                    <div className="bg-slate-700/30 rounded-xl p-4">
                      <span className="text-slate-300 font-medium block mb-2">🤖 AI Analizi</span>
                      <p className="text-slate-200 leading-relaxed">{analysisResult.analysis}</p>
                    </div>

                  </div>
                ) : (
                  <div className="text-center py-12 text-slate-400">
                    <div className="text-6xl mb-4">🔍</div>
                    <p className="text-lg">Harcamanızı analiz etmek için bilgileri girin</p>
                    <p className="text-sm mt-2">AI sistemi harcamanızı kategorize edecek ve öneriler sunacak</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Ekstre Analizi Tab */}
          {activeTab === 'upload' && (
            <div className="space-y-6">
              {/* Credit Card Statement Upload */}
              <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-8">
                <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 mb-6 flex items-center gap-3">
                  📄 Kredi Kartı Ekstresi Yükle
                </h3>
                
                {!creditCardAnalysis ? (
                  <div className="space-y-6">
                    {/* File Upload Area */}
                    <div 
                      className={`border-2 border-dashed border-slate-600 rounded-xl p-12 text-center transition-colors ${
                        selectedFile ? 'border-blue-500 bg-blue-500/10' : 'hover:border-slate-500 hover:bg-slate-700/50'
                      }`}
                      onDragOver={(e) => e.preventDefault()}
                      onDrop={(e) => {
                        e.preventDefault();
                        const file = e.dataTransfer.files[0];
                        if (file && (file.name.endsWith('.csv') || file.name.endsWith('.txt') || file.name.endsWith('.xlsx'))) {
                          setSelectedFile(file);
                        }
                      }}
                    >
                      {selectedFile ? (
                        <div className="space-y-4">
                          <div className="text-6xl">📄</div>
                          <div>
                            <h4 className="text-xl font-semibold text-white">{selectedFile.name}</h4>
                            <p className="text-slate-400">Dosya hazır - analiz etmek için butona tıklayın</p>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-4">
                          <div className="text-6xl text-slate-600">📄</div>
                          <div>
                            <h4 className="text-xl font-semibold text-white mb-2">Kredi Kartı Ekstresini Sürükle</h4>
                            <p className="text-slate-400 mb-4">CSV, TXT veya XLSX formatında ekstre dosyanızı buraya sürükleyin</p>
                            <input
                              type="file"
                              accept=".csv,.txt,.xlsx"
                              onChange={handleFileSelect}
                              className="hidden"
                              id="file-upload"
                            />
                            <label 
                              htmlFor="file-upload"
                              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg cursor-pointer hover:bg-blue-700 transition-colors"
                            >
                              Dosya Seç
                            </label>
                          </div>
                        </div>
                      )}
                    </div>

                    {selectedFile && (
                      <div className="flex justify-center">
                        <button
                          onClick={uploadCreditCardStatement}
                          disabled={isUploadingStatement}
                          className={`px-8 py-4 rounded-xl font-semibold text-lg transition-all ${
                            isUploadingStatement 
                              ? 'bg-slate-600 text-slate-400 cursor-not-allowed' 
                              : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
                          }`}
                        >
                          {isUploadingStatement ? (
                            <div className="flex items-center gap-3">
                              <div className="animate-spin w-5 h-5 border-2 border-slate-400 border-t-transparent rounded-full"></div>
                              Analiz Ediliyor...
                            </div>
                          ) : (
                            '🚀 Analiz Et'
                          )}
                        </button>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="space-y-8">
                    {/* Analysis Results */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 backdrop-blur-sm rounded-xl border border-blue-400/30 p-6">
                        <div className="text-3xl mb-3">💰</div>
                        <div className="text-2xl font-bold text-white">₺{creditCardAnalysis.summary.total_amount.toLocaleString()}</div>
                        <div className="text-slate-400">Toplam Harcama</div>
                      </div>
                      <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 backdrop-blur-sm rounded-xl border border-green-400/30 p-6">
                        <div className="text-3xl mb-3">🔢</div>
                        <div className="text-2xl font-bold text-white">{creditCardAnalysis.summary.transaction_count}</div>
                        <div className="text-slate-400">İşlem Sayısı</div>
                      </div>
                      <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 backdrop-blur-sm rounded-xl border border-purple-400/30 p-6">
                        <div className="text-3xl mb-3">📊</div>
                        <div className="text-2xl font-bold text-white">₺{creditCardAnalysis.summary.avg_transaction.toLocaleString()}</div>
                        <div className="text-slate-400">Ortalama İşlem</div>
                      </div>
                    </div>

                    {/* Top Categories */}
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-xl border border-white/10 p-6">
                      <h4 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        📈 En Çok Harcama Yapılan Kategoriler
                      </h4>
                      <div className="space-y-3">
                        {creditCardAnalysis.top_categories.map((category, index) => (
                          <div key={index} className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-sm font-bold text-white">
                                {index + 1}
                              </div>
                              <span className="text-white font-medium">{category.category}</span>
                            </div>
                            <div className="text-right">
                              <div className="text-white font-bold">₺{category.amount.toLocaleString()}</div>
                              <div className="text-slate-400 text-sm">{category.percentage}%</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Insights */}
                    <div className="bg-slate-800/30 backdrop-blur-sm rounded-xl border border-white/10 p-6">
                      <h4 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        💡 AI İçgörüleri
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {creditCardAnalysis.insights.map((insight, index) => (
                          <div key={index} className="bg-slate-700/30 rounded-lg p-4">
                            <div className="text-2xl mb-2">{insight.icon}</div>
                            <div className="text-white font-medium mb-1">{insight.title}</div>
                            <div className="text-slate-400 text-sm">{insight.message}</div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Detailed Transactions */}
                    {creditCardAnalysis.categorized_transactions && creditCardAnalysis.categorized_transactions.length > 0 && (
                      <div className="bg-slate-800/30 backdrop-blur-sm rounded-xl border border-white/10 p-6">
                        <h4 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                          📝 İşlem Detayları
                        </h4>
                        <div className="max-h-96 overflow-y-auto space-y-2">
                          {creditCardAnalysis.categorized_transactions.slice(0, 20).map((transaction, index) => (
                            <div key={index} className="bg-slate-700/30 rounded-lg p-3 flex items-center justify-between">
                              <div className="flex items-center gap-3">
                                <div className="w-6 h-6 bg-gradient-to-r from-green-400 to-blue-500 rounded-full text-xs flex items-center justify-center text-white font-bold">
                                  {index + 1}
                                </div>
                                <div>
                                  <div className="text-white font-medium text-sm">{transaction.description}</div>
                                  <div className="text-slate-400 text-xs">{transaction.category}</div>
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="text-white font-bold">₺{transaction.amount.toLocaleString()}</div>
                                <div className="text-slate-400 text-xs">{transaction.date}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                        {creditCardAnalysis.categorized_transactions.length > 20 && (
                          <div className="text-center mt-4">
                            <span className="text-slate-400 text-sm">
                              ve {creditCardAnalysis.categorized_transactions.length - 20} işlem daha...
                            </span>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Reset Button */}
                    <div className="flex justify-center">
                      <button
                        onClick={() => {
                          setCreditCardAnalysis(null);
                          setSelectedFile(null);
                        }}
                        className="bg-slate-600 text-white px-6 py-3 rounded-lg hover:bg-slate-700 transition-colors"
                      >
                        🔄 Yeni Analiz
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Aylık Özet Tab */}
          {activeTab === 'summary' && (
            <div className="space-y-6">
              {isLoadingMonthly ? (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-4 border-green-500 border-t-transparent mx-auto mb-4"></div>
                  <p className="text-slate-300 text-lg">Aylık veriler yükleniyor...</p>
                </div>
              ) : monthlyData ? (
                <>
                  {/* Özet Kartlar */}
                  <div className="grid md:grid-cols-4 gap-6">
                    <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 backdrop-blur-sm rounded-2xl border border-blue-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">💰</div>
                        <div className="text-xs text-blue-300 bg-blue-500/20 px-2 py-1 rounded-full">TOPLAM</div>
                      </div>
                      <div className="text-2xl font-bold text-white mb-1">
                        {monthlyData.total_spent.toLocaleString('tr-TR')}₺
                      </div>
                      <div className="text-blue-300 text-sm">Bu ay toplam harcama</div>
                    </div>

                    <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 backdrop-blur-sm rounded-2xl border border-green-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">📈</div>
                        <div className="text-xs text-green-300 bg-green-500/20 px-2 py-1 rounded-full">İŞLEM</div>
                      </div>
                      <div className="text-2xl font-bold text-white mb-1">
                        {monthlyData.expense_count}
                      </div>
                      <div className="text-green-300 text-sm">Toplam işlem sayısı</div>
                    </div>

                    <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 backdrop-blur-sm rounded-2xl border border-purple-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">📅</div>
                        <div className="text-xs text-purple-300 bg-purple-500/20 px-2 py-1 rounded-full">GÜNLÜK</div>
                      </div>
                      <div className="text-2xl font-bold text-white mb-1">
                        {monthlyData.average_per_day.toFixed(0)}₺
                      </div>
                      <div className="text-purple-300 text-sm">Günlük ortalama</div>
                    </div>

                    <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/20 backdrop-blur-sm rounded-2xl border border-orange-400/30 p-6">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-3xl">🏆</div>
                        <div className="text-xs text-orange-300 bg-orange-500/20 px-2 py-1 rounded-full">EN ÇOK</div>
                      </div>
                      <div className="text-lg font-bold text-white mb-1">
                        {monthlyData.top_category && monthlyData.category_summary[monthlyData.top_category]?.name || 'N/A'}
                      </div>
                      <div className="text-orange-300 text-sm">En çok harcanan kategori</div>
                    </div>
                  </div>

                  {/* Kategori Detayları */}
                  <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                    <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                      📊 Kategori Bazlı Harcamalar
                    </h3>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {Object.entries(monthlyData.category_summary).map(([key, category]: [string, any]) => (
                        <div key={key} className="bg-slate-700/30 rounded-xl p-4">
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-2">
                              <span className="text-2xl">{category.icon}</span>
                              <span className="text-white font-medium">{category.name}</span>
                            </div>
                            <span className="text-xs bg-slate-600 text-slate-300 px-2 py-1 rounded-full">
                              {category.count} işlem
                            </span>
                          </div>
                          <div className="text-2xl font-bold text-white mb-1">
                            {category.amount.toLocaleString('tr-TR')}₺
                          </div>
                          <div className="w-full bg-slate-600 rounded-full h-2 mb-2">
                            <div 
                              className="h-2 rounded-full bg-gradient-to-r from-green-500 to-emerald-600"
                              style={{ width: `${category.percentage}%` }}
                            ></div>
                          </div>
                          <div className="text-slate-400 text-sm">%{category.percentage.toFixed(1)} pay</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">📊</div>
                  <p className="text-slate-300 text-lg">Aylık özet verisi bulunamadı</p>
                </div>
              )}
            </div>
          )}

          {/* İçgörüler Tab */}
          {activeTab === 'insights' && (
            <div className="space-y-6">
              {monthlyData?.insights ? (
                <div className="grid gap-6">
                  {monthlyData.insights.map((insight, index) => (
                    <div key={index} className={`rounded-2xl border p-6 ${
                      insight.type === 'warning' 
                        ? 'bg-red-500/10 border-red-400/30' 
                        : insight.type === 'suggestion'
                        ? 'bg-blue-500/10 border-blue-400/30'
                        : 'bg-green-500/10 border-green-400/30'
                    }`}>
                      <div className="flex items-start space-x-4">
                        <div className="text-3xl">{insight.icon}</div>
                        <div className="flex-1">
                          <h3 className={`text-xl font-semibold mb-2 ${
                            insight.type === 'warning' ? 'text-red-300' : 
                            insight.type === 'suggestion' ? 'text-blue-300' : 'text-green-300'
                          }`}>
                            {insight.title}
                          </h3>
                          <p className="text-slate-200 leading-relaxed">{insight.message}</p>
                          <div className="mt-3 flex items-center space-x-2">
                            <span className={`text-xs px-2 py-1 rounded-full ${
                              insight.type === 'warning' 
                                ? 'bg-red-500/20 text-red-300' 
                                : insight.type === 'suggestion'
                                ? 'bg-blue-500/20 text-blue-300'
                                : 'bg-green-500/20 text-green-300'
                            }`}>
                              Öncelik: {insight.priority}/5
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-12 text-center">
                  <div className="text-6xl mb-4">💡</div>
                  <p className="text-slate-300 text-lg">İçgörü verisi bulunamadı</p>
                  <button
                    onClick={loadMonthlySummary}
                    className="mt-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-2 rounded-lg hover:from-green-600 hover:to-emerald-700 transition-all"
                  >
                    Verileri Yükle
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Ekstre Geçmişi Tab */}
          {activeTab === 'history' && (
            <div className="space-y-6">
              {/* Ekstre Listesi */}
              <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-semibold text-white flex items-center">
                    📋 Yüklenen Ekstreler
                  </h2>
                  <button
                    onClick={loadStatements}
                    className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all"
                  >
                    🔄 Yenile
                  </button>
                </div>

                {isLoadingStatements ? (
                  <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Ekstreler yükleniyor...</p>
                  </div>
                ) : statementList.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="text-6xl mb-4">📄</div>
                    <p className="text-slate-300 text-lg mb-2">Henüz ekstre yüklenmemiş</p>
                    <p className="text-slate-400">Ekstre analizi yapmak için "Ekstre Analizi" sekmesini kullanın</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {statementList.map((statement, index) => (
                      <div 
                        key={statement.id}
                        className="bg-slate-700/30 rounded-xl p-4 border border-white/10 hover:border-green-400/50 transition-all cursor-pointer"
                        onClick={() => loadStatementDetail(statement.id)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <span className="text-2xl">📄</span>
                              <div>
                                <h3 className="text-lg font-semibold text-white">{statement.file_name}</h3>
                                <p className="text-slate-400 text-sm">
                                  {statement.upload_date} • {statement.transaction_count} işlem
                                </p>
                              </div>
                            </div>
                          </div>
                          
                          <div className="text-right">
                            <p className="text-2xl font-bold text-green-400">
                              ₺{statement.total_amount.toLocaleString('tr-TR', {minimumFractionDigits: 2})}
                            </p>
                            <p className="text-slate-400 text-sm">
                              Ort: ₺{statement.avg_transaction.toLocaleString('tr-TR', {minimumFractionDigits: 2})}
                            </p>
                          </div>
                        </div>

                        {/* Tarih Aralığı ve En Çok Harcanan Kategori */}
                        <div className="mt-3 flex items-center justify-between text-sm">
                          <div className="flex items-center space-x-4 text-slate-400">
                            <span>📅 {statement.date_range.start} - {statement.date_range.end}</span>
                            {statement.top_category && (
                              <span className="flex items-center space-x-1">
                                <span>{statement.top_category.icon}</span>
                                <span>{statement.top_category.name}</span>
                              </span>
                            )}
                          </div>
                          <div className="flex items-center space-x-2">
                            {statement.insights_count > 0 && (
                              <span className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded-full text-xs">
                                💡 {statement.insights_count} içgörü
                              </span>
                            )}
                            <span className="text-green-400">👆 Detaylar için tıklayın</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Seçilen Ekstre Detayı */}
              {selectedStatement && (
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-semibold text-white flex items-center">
                      📊 Ekstre Detayı: {selectedStatement.file_name}
                    </h2>
                    <button
                      onClick={() => setSelectedStatement(null)}
                      className="text-slate-400 hover:text-white transition-colors"
                    >
                      ✖️ Kapat
                    </button>
                  </div>

                  {/* Özet İstatistikler */}
                  <div className="grid md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-slate-700/50 rounded-xl p-4 text-center">
                      <div className="text-2xl font-bold text-green-400 mb-1">
                        ₺{selectedStatement.summary.total_amount.toLocaleString('tr-TR', {minimumFractionDigits: 2})}
                      </div>
                      <div className="text-slate-400 text-sm">Toplam Harcama</div>
                    </div>
                    <div className="bg-slate-700/50 rounded-xl p-4 text-center">
                      <div className="text-2xl font-bold text-blue-400 mb-1">
                        {selectedStatement.summary.transaction_count}
                      </div>
                      <div className="text-slate-400 text-sm">İşlem Sayısı</div>
                    </div>
                    <div className="bg-slate-700/50 rounded-xl p-4 text-center">
                      <div className="text-2xl font-bold text-purple-400 mb-1">
                        ₺{selectedStatement.summary.avg_transaction.toLocaleString('tr-TR', {minimumFractionDigits: 2})}
                      </div>
                      <div className="text-slate-400 text-sm">Ortalama İşlem</div>
                    </div>
                    <div className="bg-slate-700/50 rounded-xl p-4 text-center">
                      <div className="text-2xl font-bold text-orange-400 mb-1">
                        {selectedStatement.summary.date_range.start} - {selectedStatement.summary.date_range.end}
                      </div>
                      <div className="text-slate-400 text-sm">Tarih Aralığı</div>
                    </div>
                  </div>

                  {/* Kategori Analizi */}
                  <div className="grid md:grid-cols-2 gap-6 mb-6">
                    {/* En Çok Harcanan Kategoriler */}
                    <div className="bg-slate-700/30 rounded-xl p-4">
                      <h3 className="text-lg font-semibold text-white mb-4">🏆 En Çok Harcanan Kategoriler</h3>
                      <div className="space-y-3">
                        {selectedStatement.top_categories.map((category, index) => (
                          <div key={index} className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <span className="text-xl">{category.icon}</span>
                              <span className="text-white">{category.name}</span>
                            </div>
                            <div className="text-right">
                              <p className="text-green-400 font-semibold">
                                ₺{category.amount.toLocaleString('tr-TR', {minimumFractionDigits: 2})}
                              </p>
                              <p className="text-slate-400 text-xs">%{category.percentage.toFixed(1)}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* İçgörüler */}
                    <div className="bg-slate-700/30 rounded-xl p-4">
                      <h3 className="text-lg font-semibold text-white mb-4">💡 AI İçgörüleri</h3>
                      <div className="space-y-3">
                        {selectedStatement.insights.slice(0, 3).map((insight, index) => (
                          <div key={index} className={`p-3 rounded-lg ${
                            insight.type === 'warning' ? 'bg-red-500/20 border-l-4 border-red-400' :
                            insight.type === 'suggestion' ? 'bg-blue-500/20 border-l-4 border-blue-400' :
                            'bg-green-500/20 border-l-4 border-green-400'
                          }`}>
                            <div className="flex items-start space-x-2">
                              <span className="text-lg">{insight.icon}</span>
                              <div>
                                <h4 className="text-white font-medium text-sm">{insight.title}</h4>
                                <p className="text-slate-300 text-xs mt-1">{insight.message}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Son İşlemler */}
                  <div className="bg-slate-700/30 rounded-xl p-4">
                    <h3 className="text-lg font-semibold text-white mb-4">📋 Son İşlemler</h3>
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {selectedStatement.categorized_transactions.slice(0, 10).map((transaction, index) => (
                        <div key={index} className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-slate-600/30">
                          <div className="flex items-center space-x-3">
                            <span className="text-sm text-slate-400">{transaction.date}</span>
                            <span className="text-white text-sm truncate max-w-xs">{transaction.description}</span>
                            <span className="text-xs px-2 py-1 rounded-full bg-slate-600 text-slate-300">
                              {transaction.category}
                            </span>
                          </div>
                          <div className="text-green-400 font-semibold">
                            ₺{transaction.amount.toLocaleString('tr-TR', {minimumFractionDigits: 2})}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default ExpenseAnalysisDashboard;
