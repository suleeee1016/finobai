import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext.tsx';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  type?: 'text' | 'analysis' | 'recommendation' | 'expense-analysis' | 'monthly-summary';
  data?: any; // Ek data için (grafikler, tablolar vb.)
}

interface ChatBotProps {
  isOpen: boolean;
  onToggle: () => void;
}

const ChatBot: React.FC<ChatBotProps> = ({ isOpen, onToggle }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Merhaba! Ben Finobai AI asistanınızım. Size nasıl yardımcı olabilirim? 🤖\n\n📊 Finansal analiz\n🏦 Kredi uygunluğu değerlendirmesi\n📈 Borsa tavsiyeleri\n💡 Bütçe optimizasyonu',
      sender: 'bot',
      timestamp: new Date(),
      type: 'text'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognition = useRef<any>(null);
  const { user } = useAuth();

  // Otomatik scroll
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Sesli tanıma başlatma
  const initSpeechRecognition = () => {
    if ('webkitSpeechRecognition' in window) {
      recognition.current = new (window as any).webkitSpeechRecognition();
      recognition.current.continuous = false;
      recognition.current.interimResults = false;
      recognition.current.lang = 'tr-TR';

      recognition.current.onstart = () => {
        setIsListening(true);
      };

      recognition.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInputMessage(transcript);
        setIsListening(false);
      };

      recognition.current.onerror = () => {
        setIsListening(false);
      };

      recognition.current.onend = () => {
        setIsListening(false);
      };
    }
  };

  useEffect(() => {
    initSpeechRecognition();
  }, []);

  // Mesaj gönderme
  const sendMessage = async (message: string = inputMessage) => {
    if (!message.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: message,
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await processMessage(message);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.text,
        sender: 'bot',
        timestamp: new Date(),
        type: (response.type as 'text' | 'analysis' | 'recommendation' | 'expense-analysis' | 'monthly-summary') || 'text',
        data: response.data
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.',
        sender: 'bot',
        timestamp: new Date(),
        type: 'text'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Harcama analizi için özel fonksiyon
  const analyzeExpense = async (expenseText: string, amount: number) => {
    try {
      const response = await fetch('http://localhost:8000/api/expenses/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          expense_text: expenseText,
          amount: amount
        })
      });

      if (!response.ok) throw new Error('Harcama analizi başarısız');

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Expense analysis error:', error);
      return null;
    }
  };

  // Aylık özet için fonksiyon  
  const getMonthlySummary = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/expenses/summary/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Aylık özet alınamadı');

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Monthly summary error:', error);
      return null;
    }
  };

  // Mesaj işleme ve AI cevap üretme
  const processMessage = async (message: string): Promise<{ text: string; type?: string; data?: any }> => {
    try {
      // Harcama analizi pattern'larını kontrol et
      const expensePattern = /(\d+(?:[.,]\d+)?)\s*₺?\s*(.+)/;
      const expenseMatch = message.match(expensePattern);

      // Aylık özet talepleri
      if (message.toLowerCase().includes('özet') || message.toLowerCase().includes('harcama') && (message.toLowerCase().includes('ay') || message.toLowerCase().includes('bu'))) {
        const summaryData = await getMonthlySummary();
        if (summaryData) {
          return {
            text: `📊 **Bu Ayın Harcama Özeti**

💰 **Toplam Harcama:** ${summaryData.total_spent.toLocaleString('tr-TR')}₺
📈 **İşlem Sayısı:** ${summaryData.expense_count}
📅 **Günlük Ortalama:** ${summaryData.average_per_day.toFixed(2)}₺

**🏆 En Çok Harcanan Kategoriler:**
${Object.entries(summaryData.category_summary)
  .sort((a: any, b: any) => b[1].amount - a[1].amount)
  .slice(0, 3)
  .map(([key, cat]: [string, any]) => `${cat.icon} ${cat.name}: ${cat.amount.toLocaleString('tr-TR')}₺`)
  .join('\n')}

**💡 Öneriler:**
${summaryData.insights.map((insight: any) => `${insight.icon} ${insight.title}: ${insight.message}`).join('\n\n')}`,
            type: 'monthly-summary',
            data: summaryData
          };
        }
      }

      // Harcama analizi (örn: "250₺ market alışverişi")
      if (expenseMatch) {
        const amount = parseFloat(expenseMatch[1].replace(',', '.'));
        const description = expenseMatch[2].trim();
        
        const analysis = await analyzeExpense(description, amount);
        if (analysis) {
          const categoryInfo = analysis.analysis.category_info;
          return {
            text: `💳 **Harcama Analizi Tamamlandı**

**📦 Kategori:** ${categoryInfo.icon} ${categoryInfo.name}
**💰 Tutar:** ${amount.toLocaleString('tr-TR')}₺
**🎯 Güven:** %${(analysis.analysis.confidence * 100).toFixed(0)}
**✅ Gereklilik:** ${analysis.analysis.is_necessary ? 'Gerekli' : 'İsteğe Bağlı'}

**🔖 Etiketler:** ${analysis.analysis.tags.join(', ')}

**📋 Analiz:** ${analysis.analysis.analysis}

**💡 Öneri:** ${analysis.suggestion}`,
            type: 'expense-analysis',
            data: analysis
          };
        }
      }

      // Normal AI chat
      const response = await fetch('http://localhost:8000/api/ai/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: message,
          conversation_id: null
        })
      });

      if (!response.ok) {
        throw new Error('AI servisi yanıt vermedi');
      }

      const data = await response.json();
      return {
        text: data.response,
        type: data.message_type || 'text'
      };
    } catch (error) {
      console.error('AI API Error:', error);
      return {
        text: 'Üzgünüm, şu anda bir teknik sorun yaşıyorum. Lütfen daha sonra tekrar deneyin.',
        type: 'text'
      };
    }
  };

  // Sesli mesaj başlatma
  const startListening = () => {
    if (recognition.current && !isListening) {
      recognition.current.start();
    }
  };

  // Quick suggestions
  const quickSuggestions = [
    "Kredi almaya uygun muyum?",
    "Hangi hisse senedine yatırım yapmalıyım?", 
    "Bütçemi nasıl optimize ederim?",
    "Bu ay harcama özetimi nedir?",
    "250₺ market alışverişi yaptım",
    "İzmir - Ankara uçak bileti 890₺"
  ];

  if (!isOpen) {
    return (
      <button
        onClick={onToggle}
        className="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full shadow-lg hover:shadow-xl transition-all z-50 flex items-center justify-center group"
      >
        <svg className="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-96 h-[32rem] bg-slate-900/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 flex flex-col z-50">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/20">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h3 className="text-white font-semibold">Finobai AI</h3>
            <p className="text-xs text-slate-400">Finansal asistanınız</p>
          </div>
        </div>
        <button
          onClick={onToggle}
          className="text-slate-400 hover:text-white transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-3 ${
              message.sender === 'user'
                ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white'
                : message.type === 'analysis'
                ? 'bg-blue-500/20 text-blue-100 border border-blue-400/30'
                : message.type === 'recommendation'
                ? 'bg-purple-500/20 text-purple-100 border border-purple-400/30'
                : message.type === 'expense-analysis'
                ? 'bg-orange-500/20 text-orange-100 border border-orange-400/30'
                : message.type === 'monthly-summary'
                ? 'bg-cyan-500/20 text-cyan-100 border border-cyan-400/30'
                : 'bg-white/10 text-slate-200 border border-white/20'
            }`}>
              <pre className="whitespace-pre-wrap text-sm font-sans leading-relaxed">
                {message.text}
              </pre>
              <div className="text-xs opacity-70 mt-2">
                {message.timestamp.toLocaleTimeString('tr-TR', { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white/10 rounded-2xl p-3 border border-white/20">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Suggestions */}
      <div className="px-4 pb-2">
        <div className="flex flex-wrap gap-2">
          {quickSuggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => sendMessage(suggestion)}
              className="text-xs bg-white/5 hover:bg-white/10 text-slate-300 px-2 py-1 rounded-lg border border-white/20 transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="p-4 border-t border-white/20">
        <div className="flex space-x-2">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Finansal sorunuzu yazın..."
              className="w-full bg-white/10 text-white placeholder-slate-400 rounded-xl px-4 py-2 border border-white/20 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
          
          <button
            onClick={startListening}
            disabled={isListening}
            className={`p-2 rounded-xl border border-white/20 transition-all ${
              isListening 
                ? 'bg-red-500/20 text-red-300 border-red-400/30' 
                : 'bg-white/5 text-slate-300 hover:bg-white/10'
            }`}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </button>

          <button
            onClick={() => sendMessage()}
            disabled={!inputMessage.trim() || isLoading}
            className="p-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
