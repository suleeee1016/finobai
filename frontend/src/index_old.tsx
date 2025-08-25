import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-blue-900 to-indigo-900">
      {/* Navigation Header */}
      <nav className="bg-white/10 backdrop-blur-md border-b border-white/20 fixed w-full top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo Section */}
            <div className="flex items-center space-x-3">
              <img src="/images/finobaai.png" alt="Finobai" className="h-12" />
            </div>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-white hover:text-blue-300 transition-colors duration-300">
                Özellikler
              </a>
              <a href="#about" className="text-white hover:text-blue-300 transition-colors duration-300">
                Hakkımızda
              </a>
              <a href="#pricing" className="text-white hover:text-blue-300 transition-colors duration-300">
                Fiyatlandırma
              </a>
              <a href="#contact" className="text-white hover:text-blue-300 transition-colors duration-300">
                İletişim
              </a>
              <div className="flex space-x-3">
                <button className="px-4 py-2 text-white border border-white/30 rounded-lg hover:bg-white/10 transition-all duration-300">
                  Giriş Yap
                </button>
                <button className="px-6 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 shadow-lg">
                  Ücretsiz Başla
                </button>
              </div>
            </div>

            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-white hover:text-blue-300 transition-colors duration-300"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {isMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 bg-white/10 backdrop-blur-md rounded-lg mt-2">
                <a href="#features" className="block px-3 py-2 text-white hover:text-blue-300 transition-colors">
                  Özellikler
                </a>
                <a href="#about" className="block px-3 py-2 text-white hover:text-blue-300 transition-colors">
                  Hakkımızda
                </a>
                <a href="#pricing" className="block px-3 py-2 text-white hover:text-blue-300 transition-colors">
                  Fiyatlandırma
                </a>
                <a href="#contact" className="block px-3 py-2 text-white hover:text-blue-300 transition-colors">
                  İletişim
                </a>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          {/* Hero Badge */}
          <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20 mb-8">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
            <span className="text-white text-sm">Yeni: AI Destekli Finansal Analiz</span>
          </div>

          {/* Main Hero Content */}
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-8 leading-tight">
            Finans Yönetiminizi
            <span className="bg-gradient-to-r from-blue-400 via-purple-500 to-indigo-600 bg-clip-text text-transparent block">
              Akıllıca Yönetin
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-blue-100 mb-12 max-w-4xl mx-auto leading-relaxed">
            Bütçenizi takip edin, yatırım kararlarınızı optimize edin ve yapay zeka destekli 
            önerilerle finansal hedeflerinize daha hızlı ulaşın. Finobai ile finans dünyasında 
            bir adım önde olun.
          </p>

          {/* Hero CTA */}
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16">
            <button className="px-8 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-lg font-semibold rounded-xl hover:from-blue-600 hover:to-indigo-700 transform hover:scale-105 transition-all duration-300 shadow-2xl">
              Ücretsiz Hesap Oluştur
            </button>
            <button className="px-8 py-4 border-2 border-white/30 text-white text-lg font-semibold rounded-xl hover:bg-white/10 transition-all duration-300 flex items-center space-x-2">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
              <span>Demo İzle</span>
            </button>
          </div>

          {/* Hero Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <div className="text-3xl font-bold text-white mb-2">50K+</div>
              <div className="text-blue-200">Aktif Kullanıcı</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <div className="text-3xl font-bold text-white mb-2">₺2.5M+</div>
              <div className="text-blue-200">Yönetilen Portföy</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <div className="text-3xl font-bold text-white mb-2">99.9%</div>
              <div className="text-blue-200">Uptime Garantisi</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-white/5 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Neden <span className="text-blue-400">Finobai?</span>
            </h2>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto">
              Modern finansal yönetim araçları ile paranızın kontrolünü tamamen elinize alın
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-gradient-to-br from-blue-500/20 to-indigo-600/20 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:border-blue-400/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-400 to-indigo-600 rounded-2xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-4">
                Akıllı Bütçe Yönetimi
              </h3>
              <p className="text-blue-100 leading-relaxed">
                Gelir ve giderlerinizi otomatik kategorilere ayırın. Hedeflerinize uygun 
                bütçe planları oluşturun ve harcama alışkanlıklarınızı optimize edin.
              </p>
            </div>

            <div className="bg-gradient-to-br from-purple-500/20 to-pink-600/20 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:border-purple-400/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-400 to-pink-600 rounded-2xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-4">
                Gerçek Zamanlı Borsa
              </h3>
              <p className="text-blue-100 leading-relaxed">
                Hisse senetleri, kripto paralar ve döviz kurlarını canlı takip edin. 
                Portföyünüzün performansını detaylı analizlerle izleyin.
              </p>
            </div>

            <div className="bg-gradient-to-br from-green-500/20 to-emerald-600/20 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:border-green-400/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-r from-green-400 to-emerald-600 rounded-2xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-4">
                Yapay Zeka Tavsiyeleri
              </h3>
              <p className="text-blue-100 leading-relaxed">
                Kişiselleştirilmiş yatırım önerileri alın. AI analizi ile risk seviyenize 
                uygun portföy önerileri ve gelecek tahminleri keşfedin.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">
            Finansal Özgürlüğünüze 
            <span className="text-blue-400"> Başlayın</span>
          </h2>
          <p className="text-xl text-blue-100 mb-12 leading-relaxed">
            Binlerce kullanıcı Finobai ile finansal hedeflerine ulaştı. 
            Siz de 30 gün ücretsiz deneme ile başlayın.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <button className="px-10 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-xl font-semibold rounded-xl hover:from-blue-600 hover:to-indigo-700 transform hover:scale-105 transition-all duration-300 shadow-2xl">
              30 Gün Ücretsiz Dene
            </button>
            <div className="text-blue-200 text-sm">
              ✓ Kredi kartı gerekmez &nbsp;&nbsp; ✓ İstediğiniz zaman iptal edin
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900/50 backdrop-blur-sm border-t border-white/10 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-3 mb-4">
                <img src="/images/finobaai.png" alt="Finobai" className="h-10" />
              </div>
              <p className="text-blue-100 mb-6 max-w-md">
                Modern teknoloji ile finansal geleceğinizi inşa edin. 
                Güvenli, hızlı ve kullanıcı dostu platform.
              </p>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Platform</h4>
              <ul className="space-y-2 text-blue-100">
                <li><button className="hover:text-white transition-colors text-left">Özellikler</button></li>
                <li><button className="hover:text-white transition-colors text-left">Güvenlik</button></li>
                <li><button className="hover:text-white transition-colors text-left">API</button></li>
                <li><button className="hover:text-white transition-colors text-left">Mobil App</button></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Destek</h4>
              <ul className="space-y-2 text-blue-100">
                <li><button className="hover:text-white transition-colors text-left">Yardım Merkezi</button></li>
                <li><button className="hover:text-white transition-colors text-left">İletişim</button></li>
                <li><button className="hover:text-white transition-colors text-left">Geri Bildirim</button></li>
                <li><button className="hover:text-white transition-colors text-left">Durum</button></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-white/10 mt-12 pt-8 text-center">
            <p className="text-blue-200">
              &copy; 2025 Finobai. Tüm hakları saklıdır. Made with ❤️ in Turkey
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <LandingPage />
  </React.StrictMode>
);
