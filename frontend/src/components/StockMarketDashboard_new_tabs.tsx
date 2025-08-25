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
                          marketSentiment.overall_sentiment.score > 0.6 ? 'text-green-400' :
                          marketSentiment.overall_sentiment.score < 0.4 ? 'text-red-400' : 'text-yellow-400'
                        }`}>
                          {marketSentiment.overall_sentiment.score > 0.6 ? '😄' :
                           marketSentiment.overall_sentiment.score < 0.4 ? '😨' : '😐'}
                        </div>
                        <h3 className="text-lg font-semibold text-white">{marketSentiment.overall_sentiment.label}</h3>
                        <p className="text-slate-300">Skor: {(marketSentiment.overall_sentiment.score * 100).toFixed(1)}/100</p>
                      </div>

                      <div className="text-center">
                        <div className="text-4xl mb-2">{
                          marketSentiment.fear_greed_index.value > 75 ? '🤑' :
                          marketSentiment.fear_greed_index.value > 50 ? '😊' :
                          marketSentiment.fear_greed_index.value > 25 ? '😐' : '😱'
                        }</div>
                        <h3 className="text-lg font-semibold text-white">Fear & Greed Index</h3>
                        <p className="text-slate-300">{marketSentiment.fear_greed_index.value}/100</p>
                        <p className={`text-sm font-medium ${
                          marketSentiment.fear_greed_index.label === 'GREED' ? 'text-red-400' :
                          marketSentiment.fear_greed_index.label === 'FEAR' ? 'text-blue-400' : 'text-yellow-400'
                        }`}>
                          {marketSentiment.fear_greed_index.label}
                        </p>
                      </div>

                      <div className="text-center">
                        <div className="text-4xl mb-2">📰</div>
                        <h3 className="text-lg font-semibold text-white">Haber Analizi</h3>
                        <p className="text-slate-300">{marketSentiment.news_analysis.total_articles} makale</p>
                        <p className="text-green-400 text-sm">
                          Pozitif: %{(marketSentiment.news_analysis.positive_ratio * 100).toFixed(1)}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Sector Sentiments */}
                  <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                    <h3 className="text-xl font-semibold text-white mb-4">🏭 Sektörel Sentiment</h3>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {Object.entries(marketSentiment.sector_sentiments).map(([sector, data]) => (
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
                              style={{ width: `${data.score * 100}%` }}
                            ></div>
                          </div>
                          <div className="text-xs text-slate-400 mt-1">
                            Skor: {(data.score * 100).toFixed(1)}
                          </div>
                        </div>
                      ))}
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
                              ₺{stock.current_price.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}
                            </div>
                            <div className="text-green-400 text-sm">
                              Hedef: ₺{stock.target_price.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}
                            </div>
                            <div className="text-blue-400 text-sm">
                              Potansiyel: +{stock.upside_potential.toFixed(1)}%
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
                              <p className="text-white font-bold">%{(stock.suggested_allocation * 100).toFixed(1)}</p>
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
