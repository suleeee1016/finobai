import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-blue-900 to-indigo-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
        
        {/* Floating particles */}
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-white rounded-full opacity-60 animate-ping"></div>
        <div className="absolute top-3/4 right-1/4 w-1 h-1 bg-blue-300 rounded-full opacity-40 animate-pulse"></div>
        <div className="absolute top-1/2 left-3/4 w-3 h-3 bg-purple-300 rounded-full opacity-30 animate-bounce"></div>
      </div>
      {/* Navigation Header */}
      <nav className="bg-white/5 backdrop-blur-xl border-b border-white/10 fixed w-full top-0 z-50 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo Section */}
            <div className="flex items-center space-x-3 group">
              <Link to="/" className="flex items-center space-x-3 transform transition-all duration-300 hover:scale-105">
                <div className="relative">
                  <img src="/images/finobaai.png" alt="Finobai" className="h-12 drop-shadow-lg" />
                  <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg blur opacity-0 group-hover:opacity-20 transition duration-300"></div>
                </div>
                <span className="text-white font-bold text-xl tracking-wide">Finobai</span>
              </Link>
            </div>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-white/80 hover:text-white hover:scale-105 transition-all duration-300 font-medium relative group">
                Özellikler
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-500 transition-all duration-300 group-hover:w-full"></span>
              </a>
              <a href="#about" className="text-white/80 hover:text-white hover:scale-105 transition-all duration-300 font-medium relative group">
                Hakkımızda
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-500 transition-all duration-300 group-hover:w-full"></span>
              </a>
              <a href="#pricing" className="text-white/80 hover:text-white hover:scale-105 transition-all duration-300 font-medium relative group">
                Fiyatlandırma
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-500 transition-all duration-300 group-hover:w-full"></span>
              </a>
              <a href="#contact" className="text-white/80 hover:text-white hover:scale-105 transition-all duration-300 font-medium relative group">
                İletişim
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-500 transition-all duration-300 group-hover:w-full"></span>
              </a>
              <div className="flex space-x-3">
                <Link
                  to="/login"
                  className="px-6 py-2.5 text-white border border-white/20 rounded-xl hover:bg-white/10 hover:border-white/40 hover:shadow-lg transition-all duration-300 font-medium backdrop-blur-sm"
                >
                  Giriş Yap
                </Link>
                <Link
                  to="/register"
                  className="px-6 py-2.5 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl hover:from-blue-600 hover:to-indigo-700 hover:scale-105 hover:shadow-2xl transition-all duration-300 font-semibold relative overflow-hidden group"
                >
                  <span className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                  <span className="relative">Ücretsiz Başla</span>
                </Link>
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
                <div className="pt-2">
                  <Link
                    to="/login"
                    className="block px-3 py-2 text-white border border-white/30 rounded-lg text-center mb-2 hover:bg-white/10 transition-all"
                  >
                    Giriş Yap
                  </Link>
                  <Link
                    to="/register"
                    className="block px-3 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg text-center hover:from-blue-600 hover:to-indigo-700 transition-all"
                  >
                    Ücretsiz Başla
                  </Link>
                </div>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          {/* Hero Badge */}
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-sm px-6 py-3 rounded-full border border-white/20 mb-8 shadow-2xl hover:scale-105 transition-all duration-300 cursor-pointer group">
            <span className="w-3 h-3 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full animate-pulse shadow-lg"></span>
            <span className="text-white text-sm font-medium group-hover:text-green-300 transition-colors duration-300">✨ Yeni: AI Destekli Finansal Analiz</span>
            <svg className="w-4 h-4 text-white/60 group-hover:text-white group-hover:translate-x-1 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>

          {/* Main Hero Content */}
          <h1 className="text-6xl md:text-8xl font-bold text-white mb-8 leading-tight">
            <span className="inline-block hover:scale-105 transition-transform duration-300">Finans</span>{' '}
            <span className="inline-block hover:scale-105 transition-transform duration-300">Yönetiminizi</span>
            <span className="bg-gradient-to-r from-blue-400 via-purple-500 to-indigo-600 bg-clip-text text-transparent block animate-gradient-x bg-300% hover:scale-105 transition-transform duration-300">
              Akıllıca Yönetin
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-blue-100/90 mb-12 max-w-4xl mx-auto leading-relaxed font-light">
            <span className="font-semibold text-white">Bütçenizi takip edin</span>, yatırım kararlarınızı optimize edin ve 
            <span className="bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent font-semibold"> yapay zeka destekli </span>
            önerilerle finansal hedeflerinize daha hızlı ulaşın. 
            <span className="text-blue-300 font-semibold">Finobai</span> ile finans dünyasında bir adım önde olun.
          </p>

          {/* Hero CTA */}
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16">
            <Link
              to="/register"
              className="group relative px-10 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-lg font-semibold rounded-2xl hover:from-blue-600 hover:to-indigo-700 transform hover:scale-105 transition-all duration-300 shadow-2xl hover:shadow-blue-500/25 overflow-hidden"
            >
              <span className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></span>
              <span className="relative flex items-center space-x-2">
                <span>🚀 Ücretsiz Hesap Oluştur</span>
              </span>
            </Link>
            <button className="group px-8 py-4 border-2 border-white/20 text-white text-lg font-semibold rounded-2xl hover:bg-white/5 hover:border-white/40 transition-all duration-300 flex items-center space-x-3 backdrop-blur-sm hover:shadow-xl">
              <div className="relative w-6 h-6 flex items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full opacity-20 group-hover:opacity-40 transition-opacity duration-300"></div>
                <svg className="w-5 h-5 relative z-10 group-hover:scale-110 transition-transform duration-300" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
              <span className="group-hover:text-blue-300 transition-colors duration-300">Demo İzle</span>
            </button>
          </div>

          {/* Hero Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="group bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-green-400/30 hover:bg-white/10 transition-all duration-300 hover:scale-105 hover:shadow-2xl cursor-pointer">
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text mb-2 group-hover:scale-110 transition-transform duration-300">50K+</div>
              <div className="text-blue-200 group-hover:text-white transition-colors duration-300">Aktif Kullanıcı</div>
              <div className="mt-2 text-xs text-green-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300">📈 +15% bu ay</div>
            </div>
            <div className="group bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-blue-400/30 hover:bg-white/10 transition-all duration-300 hover:scale-105 hover:shadow-2xl cursor-pointer">
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text mb-2 group-hover:scale-110 transition-transform duration-300">₺2.5M+</div>
              <div className="text-blue-200 group-hover:text-white transition-colors duration-300">Yönetilen Portföy</div>
              <div className="mt-2 text-xs text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300">💼 Güvenli & Hızlı</div>
            </div>
            <div className="group bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-purple-400/30 hover:bg-white/10 transition-all duration-300 hover:scale-105 hover:shadow-2xl cursor-pointer">
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text mb-2 group-hover:scale-110 transition-transform duration-300">99.9%</div>
              <div className="text-blue-200 group-hover:text-white transition-colors duration-300">Uptime Garantisi</div>
              <div className="mt-2 text-xs text-purple-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300">⚡ 7/24 Aktif</div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-white/5 to-blue-900/10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-green-500/10 to-emerald-500/10 backdrop-blur-sm px-6 py-3 rounded-full border border-green-400/20 mb-8">
            <span className="w-3 h-3 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full animate-pulse"></span>
            <span className="text-white text-sm font-medium">🏆 Türkiye'nin En Güvenilir Fintech Platformu</span>
          </div>
          
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-12">
            🌟 Binlerce Kullanıcı <span className="text-green-400">Finobai'ye</span> Güveniyor
          </h2>

          {/* Testimonials */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-blue-400/40 transition-all duration-300 hover:scale-105 group">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-400 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">M</div>
                <div>
                  <div className="text-white font-semibold">Mehmet K.</div>
                  <div className="text-blue-200 text-sm">Girişimci</div>
                </div>
              </div>
              <div className="text-yellow-400 mb-3">⭐⭐⭐⭐⭐</div>
              <p className="text-blue-100 italic group-hover:text-white transition-colors duration-300">
                "Harcama analizim sayesinde ayda 1500₺ tasarruf etmeye başladım. AI önerileri gerçekten işe yarar!"
              </p>
            </div>

            <div className="bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-green-400/40 transition-all duration-300 hover:scale-105 group">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-green-400 to-emerald-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">A</div>
                <div>
                  <div className="text-white font-semibold">Ayşe D.</div>
                  <div className="text-blue-200 text-sm">Öğretmen</div>
                </div>
              </div>
              <div className="text-yellow-400 mb-3">⭐⭐⭐⭐⭐</div>
              <p className="text-blue-100 italic group-hover:text-white transition-colors duration-300">
                "Ekstre yükleme özelliği hayat kurtarıcı. 6 aylık harcamalarımı 5 dakikada analiz etti!"
              </p>
            </div>

            <div className="bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-purple-400/40 transition-all duration-300 hover:scale-105 group">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-pink-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">C</div>
                <div>
                  <div className="text-white font-semibold">Can S.</div>
                  <div className="text-blue-200 text-sm">Yazılım Geliştirici</div>
                </div>
              </div>
              <div className="text-yellow-400 mb-3">⭐⭐⭐⭐⭐</div>
              <p className="text-blue-100 italic group-hover:text-white transition-colors duration-300">
                "Borsa analizi modülleri sayesinde yatırım kararlarımı çok daha bilinçli veriyorum."
              </p>
            </div>
          </div>

          {/* Trust Indicators */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center group hover:scale-110 transition-all duration-300 cursor-pointer">
              <div className="text-3xl mb-2 group-hover:animate-bounce">🔒</div>
              <div className="text-white font-semibold group-hover:text-blue-300 transition-colors duration-300">256-bit SSL</div>
              <div className="text-blue-200 text-sm">Banka Seviyesi Güvenlik</div>
            </div>
            <div className="text-center group hover:scale-110 transition-all duration-300 cursor-pointer">
              <div className="text-3xl mb-2 group-hover:animate-bounce">🏦</div>
              <div className="text-white font-semibold group-hover:text-green-300 transition-colors duration-300">BDDK Uyumlu</div>
              <div className="text-blue-200 text-sm">Resmi Düzenlemelere Uygun</div>
            </div>
            <div className="text-center group hover:scale-110 transition-all duration-300 cursor-pointer">
              <div className="text-3xl mb-2 group-hover:animate-bounce">🏅</div>
              <div className="text-white font-semibold group-hover:text-yellow-300 transition-colors duration-300">FinTech Ödülü</div>
              <div className="text-blue-200 text-sm">2024 En İyi Platform</div>
            </div>
            <div className="text-center group hover:scale-110 transition-all duration-300 cursor-pointer">
              <div className="text-3xl mb-2 group-hover:animate-bounce">⚡</div>
              <div className="text-white font-semibold group-hover:text-purple-300 transition-colors duration-300">99.9% Uptime</div>
              <div className="text-blue-200 text-sm">7/24 Kesintisiz Hizmet</div>
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
              Dashboard'unuzda bulunan güçlü araçlarla finansal yönetiminizi tamamen kontrol altına alın
            </p>
            <div className="mt-8 inline-flex items-center space-x-2 bg-gradient-to-r from-blue-500/10 to-purple-500/10 backdrop-blur-sm px-6 py-3 rounded-full border border-blue-400/20">
              <span className="text-blue-300">🎯</span>
              <span className="text-white font-medium">6 Ana Özellik • 5 Ultra AI Modülü • Sınırsız Analiz</span>
            </div>
          </div>

          {/* Ana Dashboard Özellikleri */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {/* Harcama Analizi */}
            <div className="group bg-gradient-to-br from-green-500/10 to-emerald-600/10 backdrop-blur-sm p-8 rounded-3xl border border-green-400/20 hover:border-green-400/60 transition-all duration-500 hover:transform hover:scale-105 hover:rotate-1 hover:shadow-2xl hover:shadow-green-500/20 cursor-pointer relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-green-400/5 to-emerald-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="w-20 h-20 bg-gradient-to-r from-green-400 to-emerald-600 rounded-3xl flex items-center justify-center mb-6 shadow-2xl group-hover:scale-110 group-hover:rotate-12 transition-all duration-500 animate-float">
                  <span className="text-3xl filter drop-shadow-lg">🔍</span>
                </div>
                <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-green-300 transition-colors duration-300">
                  AI Harcama Analizi
                </h3>
                <p className="text-blue-100 leading-relaxed mb-4 group-hover:text-white transition-colors duration-300">
                  Harcamalarınızı doğal dil ile yazın, yapay zeka otomatik olarak kategorilere ayırsın. 
                  "Migros'tan alışveriş 250₺" yazmanız yeterli!
                </p>
                <ul className="text-sm text-green-200 space-y-2">
                  <li className="flex items-center space-x-2 group-hover:text-green-100 transition-colors duration-300">
                    <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></span>
                    <span>Akıllı kategori önerileri</span>
                  </li>
                  <li className="flex items-center space-x-2 group-hover:text-green-100 transition-colors duration-300">
                    <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></span>
                    <span>%95+ güven oranı</span>
                  </li>
                  <li className="flex items-center space-x-2 group-hover:text-green-100 transition-colors duration-300">
                    <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></span>
                    <span>Otomatik etiketleme</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Ekstre Analizi */}
            <div className="group bg-gradient-to-br from-blue-500/10 to-indigo-600/10 backdrop-blur-sm p-8 rounded-3xl border border-blue-400/20 hover:border-blue-400/60 transition-all duration-500 hover:transform hover:scale-105 hover:-rotate-1 hover:shadow-2xl hover:shadow-blue-500/20 cursor-pointer relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-400/5 to-indigo-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-400 to-indigo-600 rounded-3xl flex items-center justify-center mb-6 shadow-2xl group-hover:scale-110 group-hover:-rotate-12 transition-all duration-500 animate-float animation-delay-1000">
                  <span className="text-3xl filter drop-shadow-lg">📄</span>
                </div>
                <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-blue-300 transition-colors duration-300">
                  Kredi Kartı Ekstresi
                </h3>
                <p className="text-blue-100 leading-relaxed mb-4 group-hover:text-white transition-colors duration-300">
                  CSV, TXT, XLSX formatlarındaki ekstrelerinizi yükleyin. AI tüm işlemleri analiz edip 
                  kategorilere ayırsın.
                </p>
                <ul className="text-sm text-blue-200 space-y-2">
                  <li className="flex items-center space-x-2 group-hover:text-blue-100 transition-colors duration-300">
                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
                    <span>Çoklu format desteği</span>
                  </li>
                  <li className="flex items-center space-x-2 group-hover:text-blue-100 transition-colors duration-300">
                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
                    <span>Otomatik kategorilendirme</span>
                  </li>
                  <li className="flex items-center space-x-2 group-hover:text-blue-100 transition-colors duration-300">
                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
                    <span>Harcama pattern analizi</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Aylık Özet */}
            <div className="bg-gradient-to-br from-purple-500/20 to-pink-600/20 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:border-purple-400/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-400 to-pink-600 rounded-2xl flex items-center justify-center mb-6">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-4">
                Aylık Özet & Raporlar
              </h3>
              <p className="text-blue-100 leading-relaxed mb-4">
                Gerçek verilerinizden oluşan detaylı aylık raporlar. Kategori bazlı analiz, 
                trend grafikleri ve karşılaştırmalar.
              </p>
              <ul className="text-sm text-purple-200 space-y-1">
                <li>• Kategori bazlı breakdown</li>
                <li>• Günlük ortalama hesaplama</li>
                <li>• Karşılaştırmalı analizler</li>
              </ul>
            </div>

            {/* AI İçgörüler */}
            <div className="bg-gradient-to-br from-amber-500/20 to-orange-600/20 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:border-amber-400/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-r from-amber-400 to-orange-600 rounded-2xl flex items-center justify-center mb-6">
                <span className="text-2xl">💡</span>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-4">
                Yapay Zeka İçgörüleri
              </h3>
              <p className="text-blue-100 leading-relaxed mb-4">
                Harcama alışkanlıklarınızı analiz eden AI, kişiselleştirilmiş tasarruf önerileri 
                ve uyarılar sunar.
              </p>
              <ul className="text-sm text-amber-200 space-y-1">
                <li>• Kişiselleştirilmiş öneriler</li>
                <li>• Tasarruf fırsatları</li>
                <li>• Harcama uyarıları</li>
              </ul>
            </div>

            {/* Ekstre Geçmişi */}
            <div className="bg-gradient-to-br from-teal-500/20 to-cyan-600/20 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:border-teal-400/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-r from-teal-400 to-cyan-600 rounded-2xl flex items-center justify-center mb-6">
                <span className="text-2xl">📋</span>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-4">
                Ekstre Geçmişi
              </h3>
              <p className="text-blue-100 leading-relaxed mb-4">
                Yüklediğiniz tüm ekstreleri saklayın, istediğiniz zaman tekrar inceleyin. 
                Geçmiş analizlerinize kolayca erişin.
              </p>
              <ul className="text-sm text-teal-200 space-y-1">
                <li>• Sınırsız ekstre saklama</li>
                <li>• Hızlı arama ve filtreleme</li>
                <li>• Detaylı analiz tekrarı</li>
              </ul>
            </div>

            {/* Borsa Takibi */}
            <div className="bg-gradient-to-br from-red-500/20 to-rose-600/20 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:border-red-400/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-r from-red-400 to-rose-600 rounded-2xl flex items-center justify-center mb-6">
                <span className="text-2xl">📈</span>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-4">
                Canlı Borsa Takibi
              </h3>
              <p className="text-blue-100 leading-relaxed mb-4">
                BIST, kripto para ve forex piyasalarını gerçek zamanlı takip edin. 
                Ultra gelişmiş AI analiz araçları ile piyasaları anlayın.
              </p>
              <ul className="text-sm text-red-200 space-y-1">
                <li>• Gerçek zamanlı veriler</li>
                <li>• AI destekli tahminler</li>
                <li>• Çoklu piyasa desteği</li>
              </ul>
            </div>
          </div>

          {/* AI Analiz Özellikleri */}
          <div className="bg-gradient-to-r from-indigo-500/10 to-purple-600/10 backdrop-blur-sm p-12 rounded-3xl border border-white/20 mb-16">
            <div className="text-center mb-12">
              <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">
                🤖 Ultra Gelişmiş AI Analiz Araçları
              </h3>
              <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                Dashboard'unuzda bulunan 5 farklı ultra analiz modülü ile piyasaları derinlemesine anlayın
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                <div className="text-3xl mb-3">🎯</div>
                <h4 className="text-lg font-semibold text-white mb-2">Temel Analiz</h4>
                <p className="text-blue-100 text-sm">Şirket mali tablolarını AI ile analiz edin, değerleme metrikleri keşfedin</p>
              </div>
              
              <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                <div className="text-3xl mb-3">📊</div>
                <h4 className="text-lg font-semibold text-white mb-2">Teknik Analiz</h4>
                <p className="text-blue-100 text-sm">Grafik patternleri, indikatörler ve trend analizleri otomatik olarak</p>
              </div>
              
              <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                <div className="text-3xl mb-3">💭</div>
                <h4 className="text-lg font-semibold text-white mb-2">Sentiment Analizi</h4>
                <p className="text-blue-100 text-sm">Sosyal medya, haberler ve piyasa duygularını AI ile ölçün</p>
              </div>
              
              <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                <div className="text-3xl mb-3">🔮</div>
                <h4 className="text-lg font-semibold text-white mb-2">Fiyat Tahmini</h4>
                <p className="text-blue-100 text-sm">Makine öğrenmesi ile gelecek fiyat tahminleri ve senaryolar</p>
              </div>
              
              <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                <div className="text-3xl mb-3">⚠️</div>
                <h4 className="text-lg font-semibold text-white mb-2">Risk Analizi</h4>
                <p className="text-blue-100 text-sm">Volatilite, korelasyon ve portföy risk hesaplamaları</p>
              </div>
              
              <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                <div className="text-3xl mb-3">🎯</div>
                <h4 className="text-lg font-semibold text-white mb-2">Hedef Analizi</h4>
                <p className="text-blue-100 text-sm">Analitik hedef fiyatları, destek-direnç seviyeleri</p>
              </div>
            </div>
          </div>

          {/* Özellik Vurguları */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-16">
            <div>
              <h3 className="text-3xl font-bold text-white mb-6">
                💳 Ekstre Analizi Nasıl Çalışır?
              </h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">1</div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">Dosya Yükle</h4>
                    <p className="text-blue-100">CSV, TXT veya XLSX formatında ekstre dosyanızı yükleyin</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">2</div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">AI Analizi</h4>
                    <p className="text-blue-100">Her işlem AI tarafından otomatik kategorilere ayrılır</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">3</div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">İçgörüler</h4>
                    <p className="text-blue-100">Kişiselleştirilmiş tasarruf önerileri ve uyarılar alın</p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-3xl font-bold text-white mb-6">
                📊 Desteklenen Analizler
              </h3>
              <div className="space-y-3">
                <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-green-400">✓</span>
                    <span className="text-white font-semibold">Kategori Bazlı Harcama</span>
                  </div>
                  <p className="text-blue-100 text-sm">Gıda, ulaşım, eğlence gibi 10+ kategori</p>
                </div>
                <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-green-400">✓</span>
                    <span className="text-white font-semibold">Trend Analizi</span>
                  </div>
                  <p className="text-blue-100 text-sm">Aylık, haftalık harcama trendleri</p>
                </div>
                <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-green-400">✓</span>
                    <span className="text-white font-semibold">Tasarruf Önerileri</span>
                  </div>
                  <p className="text-blue-100 text-sm">AI destekli kişisel tasarruf planları</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-900 to-slate-800 relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl animate-pulse animation-delay-2000"></div>
        </div>
        
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-green-500/10 to-emerald-500/10 backdrop-blur-sm px-6 py-3 rounded-full border border-green-400/20 mb-8">
              <span className="text-2xl">💎</span>
              <span className="text-white font-semibold">Şeffaf ve Adil Fiyatlandırma</span>
            </div>
            
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
              <span className="bg-gradient-to-r from-green-400 via-blue-500 to-purple-600 bg-clip-text text-transparent animate-gradient-x bg-300%">
                Herkes İçin Uygun
              </span>
            </h2>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto leading-relaxed">
              30 gün ücretsiz deneyin. Istediğiniz zaman iptal edin. Gizli ücret yok, taahhüt yok.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Free Plan */}
            <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-blue-400/50 transition-all duration-500 hover:scale-105 hover:shadow-2xl relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-400/5 to-cyan-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="text-center mb-8">
                  <div className="text-4xl mb-4">🆓</div>
                  <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-blue-300 transition-colors duration-300">
                    Başlangıç
                  </h3>
                  <div className="text-4xl font-bold text-white mb-2">
                    ₺0<span className="text-lg text-blue-200">/ay</span>
                  </div>
                  <p className="text-blue-200 group-hover:text-blue-100 transition-colors duration-300">
                    30 gün ücretsiz deneme
                  </p>
                </div>

                <ul className="space-y-4 mb-8">
                  <li className="flex items-center space-x-3 text-blue-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    <span>Temel harcama analizi</span>
                  </li>
                  <li className="flex items-center space-x-3 text-blue-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    <span>Aylık 10 ekstre işlemi</span>
                  </li>
                  <li className="flex items-center space-x-3 text-blue-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    <span>Basit raporlar</span>
                  </li>
                  <li className="flex items-center space-x-3 text-blue-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    <span>Email desteği</span>
                  </li>
                </ul>

                <Link
                  to="/register"
                  className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 transform hover:scale-105 block text-center group-hover:shadow-lg"
                >
                  Ücretsiz Başla
                </Link>
              </div>
            </div>

            {/* Pro Plan - Most Popular */}
            <div className="group bg-gradient-to-br from-white/10 to-white/20 backdrop-blur-xl rounded-3xl p-8 border-2 border-gradient-to-r from-yellow-400 to-orange-500 hover:border-yellow-300 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-yellow-500/20 relative overflow-hidden transform scale-105">
              <div className="absolute inset-0 bg-gradient-to-br from-yellow-400/5 to-orange-600/5 opacity-50 group-hover:opacity-70 transition-opacity duration-500"></div>
              
              {/* Popular Badge */}
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div className="bg-gradient-to-r from-yellow-400 to-orange-500 text-black px-6 py-2 rounded-full text-sm font-bold animate-pulse">
                  🔥 EN POPÜLER
                </div>
              </div>

              <div className="relative z-10">
                <div className="text-center mb-8 pt-4">
                  <div className="text-4xl mb-4">⭐</div>
                  <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-yellow-300 transition-colors duration-300">
                    Profesyonel
                  </h3>
                  <div className="text-4xl font-bold text-white mb-2">
                    ₺49<span className="text-lg text-yellow-200">/ay</span>
                  </div>
                  <p className="text-yellow-200 group-hover:text-yellow-100 transition-colors duration-300">
                    İlk ay %50 indirim - ₺24.5
                  </p>
                </div>

                <ul className="space-y-4 mb-8">
                  <li className="flex items-center space-x-3 text-yellow-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                    <span><strong>Tüm başlangıç özellikleri</strong></span>
                  </li>
                  <li className="flex items-center space-x-3 text-yellow-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                    <span>🤖 5 Ultra AI Analiz Modülü</span>
                  </li>
                  <li className="flex items-center space-x-3 text-yellow-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                    <span>📊 Sınırsız ekstre işlemi</span>
                  </li>
                  <li className="flex items-center space-x-3 text-yellow-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                    <span>📈 Canlı borsa takibi</span>
                  </li>
                  <li className="flex items-center space-x-3 text-yellow-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                    <span>🎯 Kişisel AI asistanı</span>
                  </li>
                  <li className="flex items-center space-x-3 text-yellow-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                    <span>📱 Öncelikli destek</span>
                  </li>
                </ul>

                <Link
                  to="/register"
                  className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black py-3 px-6 rounded-xl font-bold hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 transform hover:scale-105 block text-center group-hover:shadow-xl shadow-yellow-500/20"
                >
                  Pro'ya Geç
                </Link>
              </div>
            </div>

            {/* Enterprise Plan */}
            <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-purple-400/50 transition-all duration-500 hover:scale-105 hover:shadow-2xl relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-purple-400/5 to-pink-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="text-center mb-8">
                  <div className="text-4xl mb-4">🏢</div>
                  <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-purple-300 transition-colors duration-300">
                    Kurumsal
                  </h3>
                  <div className="text-4xl font-bold text-white mb-2">
                    ₺199<span className="text-lg text-purple-200">/ay</span>
                  </div>
                  <p className="text-purple-200 group-hover:text-purple-100 transition-colors duration-300">
                    Şirketler için özel çözüm
                  </p>
                </div>

                <ul className="space-y-4 mb-8">
                  <li className="flex items-center space-x-3 text-purple-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></span>
                    <span><strong>Tüm Pro özellikleri</strong></span>
                  </li>
                  <li className="flex items-center space-x-3 text-purple-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></span>
                    <span>👥 Çoklu kullanıcı</span>
                  </li>
                  <li className="flex items-center space-x-3 text-purple-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></span>
                    <span>🔧 API erişimi</span>
                  </li>
                  <li className="flex items-center space-x-3 text-purple-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></span>
                    <span>📊 Özel raporlar</span>
                  </li>
                  <li className="flex items-center space-x-3 text-purple-100 group-hover:text-white transition-colors duration-300">
                    <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></span>
                    <span>☎️ 7/24 telefon desteği</span>
                  </li>
                </ul>

                <Link
                  to="/register"
                  className="w-full bg-gradient-to-r from-purple-500 to-pink-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-purple-600 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 block text-center group-hover:shadow-lg"
                >
                  İletişime Geç
                </Link>
              </div>
            </div>
          </div>

          {/* Pricing Features */}
          <div className="mt-16 text-center">
            <p className="text-blue-100 mb-8">
              ✅ Tüm planlar için: SSL güvenlik • Otomatik yedekleme • 99.9% uptime garantisi
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <div className="bg-white/5 p-4 rounded-xl backdrop-blur-sm border border-white/10">
                <div className="text-2xl mb-2">💳</div>
                <div className="text-white font-semibold mb-1">Güvenli Ödeme</div>
                <div className="text-blue-200 text-sm">256-bit SSL şifrelemesi</div>
              </div>
              <div className="bg-white/5 p-4 rounded-xl backdrop-blur-sm border border-white/10">
                <div className="text-2xl mb-2">🔄</div>
                <div className="text-white font-semibold mb-1">İstediğiniz Zaman İptal</div>
                <div className="text-blue-200 text-sm">Taahhüt ve ceza yok</div>
              </div>
              <div className="bg-white/5 p-4 rounded-xl backdrop-blur-sm border border-white/10">
                <div className="text-2xl mb-2">🎁</div>
                <div className="text-white font-semibold mb-1">30 Gün Garanti</div>
                <div className="text-blue-200 text-sm">Memnun kalmazsan para iade</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-900/20 to-purple-900/20 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-10 left-10 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-10 right-10 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl animate-pulse animation-delay-2000"></div>
        </div>
        
        <div className="max-w-6xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-orange-500/10 to-red-500/10 backdrop-blur-sm px-6 py-3 rounded-full border border-orange-400/20 mb-8 animate-bounce">
            <span className="text-2xl">🚀</span>
            <span className="text-white font-semibold">Canlı Demo ile Keşfedin</span>
          </div>
          
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-8 leading-tight">
            <span className="bg-gradient-to-r from-orange-400 via-red-500 to-pink-600 bg-clip-text text-transparent animate-gradient-x bg-300%">
              Dashboard'unuzda Sizi Bekliyor
            </span>
          </h2>
          <p className="text-xl text-blue-100 mb-12 max-w-3xl mx-auto leading-relaxed">
            Tüm bu güçlü özellikler Dashboard'unuzda sizi bekliyor. 
            <span className="text-white font-semibold"> Hemen kaydolun</span> ve finansal geleceğinizi şekillendirmeye başlayın!
          </p>
          
          <div className="bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 shadow-2xl hover:shadow-3xl transition-all duration-500 hover:scale-105 group">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <div className="group/item hover:scale-110 transition-all duration-300 cursor-pointer">
                <div className="text-5xl font-bold text-transparent bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text mb-2 group-hover/item:animate-pulse">30s</div>
                <div className="text-blue-100 group-hover/item:text-white transition-colors duration-300">⚡ Kayıt Süresi</div>
                <div className="text-xs text-green-400 mt-1 opacity-70">Anında başlayın</div>
              </div>
              <div className="group/item hover:scale-110 transition-all duration-300 cursor-pointer">
                <div className="text-5xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text mb-2 group-hover/item:animate-pulse">5</div>
                <div className="text-blue-100 group-hover/item:text-white transition-colors duration-300">🤖 Ultra Analiz Modülü</div>
                <div className="text-xs text-blue-400 mt-1 opacity-70">AI destekli</div>
              </div>
              <div className="group/item hover:scale-110 transition-all duration-300 cursor-pointer">
                <div className="text-5xl font-bold text-transparent bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text mb-2 group-hover/item:animate-pulse">∞</div>
                <div className="text-blue-100 group-hover/item:text-white transition-colors duration-300">📊 Sınırsız Analiz</div>
                <div className="text-xs text-purple-400 mt-1 opacity-70">Her zaman güncel</div>
              </div>
            </div>
            
            <div className="mt-8 flex justify-center">
              <Link
                to="/register"
                className="group/cta inline-flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-orange-500 to-red-600 text-white text-lg font-semibold rounded-2xl hover:from-orange-600 hover:to-red-700 transform hover:scale-105 transition-all duration-300 shadow-2xl hover:shadow-orange-500/25 relative overflow-hidden"
              >
                <span className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover/cta:opacity-100 transition-opacity duration-300 rounded-2xl"></span>
                <span className="relative">🎯 Hemen Başla</span>
                <svg className="w-5 h-5 relative group-hover/cta:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-800 to-slate-900">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 backdrop-blur-sm px-6 py-3 rounded-full border border-cyan-400/20 mb-8">
              <span className="text-2xl">❓</span>
              <span className="text-white font-semibold">Sıkça Sorulan Sorular</span>
            </div>
            
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                Merak Ettikleriniz
              </span>
            </h2>
            <p className="text-xl text-blue-100">
              En çok sorulan soruları derledik. Daha fazla bilgi için destek ekibimizle iletişime geçebilirsiniz.
            </p>
          </div>

          <div className="space-y-6">
            {[
              {
                question: "🔒 Finansal verilerim güvende mi?",
                answer: "Evet, tüm verileriniz 256-bit SSL şifreleme ile korunur. Banka seviyesi güvenlik protokolleri kullanıyoruz ve hiçbir zaman kişisel verilerinizi üçüncü taraflarla paylaşmayız."
              },
              {
                question: "🤖 AI nasıl çalışıyor? Ne kadar doğru?",
                answer: "Yapay zeka sistemimiz, milyonlarca işlem verisi ile eğitilmiştir ve %95+ doğruluk oranına sahiptir. Harcamalarınızı otomatik kategorilere ayırır ve kişiselleştirilmiş öneriler sunar."
              },
              {
                question: "📄 Hangi ekstre formatları destekleniyor?",
                answer: "CSV, TXT, XLSX, PDF formatlarındaki ekstreleri yükleyebilirsiniz. Tüm büyük bankaların ekstre formatları desteklenir (Garanti, İş Bankası, Akbank, Yapı Kredi vb.)."
              },
              {
                question: "💳 Ücretsiz deneme nasıl çalışır?",
                answer: "30 gün boyunca tüm Pro özelliklerini ücretsiz kullanabilirsiniz. Kredi kartı bilgisi gerekmez, istediğiniz zaman iptal edebilirsiniz."
              },
              {
                question: "📱 Mobil uygulama var mı?",
                answer: "Şu anda web tabanlı platform sunuyoruz. iOS ve Android uygulamaları 2025 yılı içinde yayınlanacak. Web sitemiz mobil uyumlu olarak tasarlanmıştır."
              },
              {
                question: "🔄 Verileri nasıl dışa aktarırım?",
                answer: "Analizlerinizi CSV, PDF veya Excel formatında dışa aktarabilirsiniz. Tüm verilerinizin sahibi sizsiniz ve istediğiniz zaman indirebilirsiniz."
              }
            ].map((faq, index) => (
              <div key={index} className="group bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 hover:border-blue-400/30 transition-all duration-300 hover:shadow-xl cursor-pointer">
                <div className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-white mb-3 group-hover:text-blue-300 transition-colors duration-300">
                        {faq.question}
                      </h3>
                      <p className="text-blue-100 leading-relaxed group-hover:text-white transition-colors duration-300">
                        {faq.answer}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <p className="text-blue-200 mb-6">Başka sorularınız mı var?</p>
            <Link
              to="/register"
              className="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold rounded-xl hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 hover:scale-105"
            >
              <span>💬 Destek Ekibiyle İletişime Geç</span>
            </Link>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-indigo-900/30 to-purple-900/30 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-72 h-72 bg-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse animation-delay-3000"></div>
        </div>
        
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 backdrop-blur-sm px-6 py-3 rounded-full border border-indigo-400/20 mb-8">
              <span className="text-2xl">🏢</span>
              <span className="text-white font-semibold">Finobai Hakkında</span>
            </div>
            
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-8">
              <span className="bg-gradient-to-r from-indigo-400 via-purple-500 to-pink-600 bg-clip-text text-transparent animate-gradient-x bg-300%">
                Türkiye'nin En Yenilikçi
              </span>
              <br />
              <span className="text-white">FinTech Platformu</span>
            </h2>
            <p className="text-xl text-blue-100 max-w-4xl mx-auto leading-relaxed">
              2024 yılında kurulan Finobai, yapay zeka destekli finansal analizler ile 
              kullanıcılarına kişiselleştirilmiş finansal çözümler sunmaktadır.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-20">
            <div>
              <h3 className="text-3xl font-bold text-white mb-6">🎯 Misyonumuz</h3>
              <p className="text-blue-100 text-lg leading-relaxed mb-6">
                Finansal okuryazarlığı yaygınlaştırmak ve herkesin bilinçli finansal 
                kararlar alabilmesini sağlamak. Modern teknoloji ile karmaşık finansal 
                analizleri herkese erişilebilir kılmak.
              </p>
              <ul className="space-y-3">
                <li className="flex items-center space-x-3 text-indigo-200">
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse"></span>
                  <span>🚀 Teknoloji odaklı çözümler</span>
                </li>
                <li className="flex items-center space-x-3 text-indigo-200">
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse"></span>
                  <span>🔐 Güvenlik ve gizlilik önceliği</span>
                </li>
                <li className="flex items-center space-x-3 text-indigo-200">
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse"></span>
                  <span>💡 Sürekli inovasyon</span>
                </li>
              </ul>
            </div>
            
            <div className="bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-indigo-400/40 transition-all duration-300 hover:scale-105">
              <div className="grid grid-cols-2 gap-6 text-center">
                <div className="group hover:scale-110 transition-all duration-300">
                  <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-indigo-400 to-purple-500 bg-clip-text mb-2 group-hover:animate-pulse">2024</div>
                  <div className="text-indigo-200 group-hover:text-white transition-colors duration-300">Kuruluş Yılı</div>
                </div>
                <div className="group hover:scale-110 transition-all duration-300">
                  <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text mb-2 group-hover:animate-pulse">50K+</div>
                  <div className="text-indigo-200 group-hover:text-white transition-colors duration-300">Aktif Kullanıcı</div>
                </div>
                <div className="group hover:scale-110 transition-all duration-300">
                  <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text mb-2 group-hover:animate-pulse">₺2.5M</div>
                  <div className="text-indigo-200 group-hover:text-white transition-colors duration-300">Analiz Edilen Portföy</div>
                </div>
                <div className="group hover:scale-110 transition-all duration-300">
                  <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text mb-2 group-hover:animate-pulse">15+</div>
                  <div className="text-indigo-200 group-hover:text-white transition-colors duration-300">Uzman Ekip</div>
                </div>
              </div>
            </div>
          </div>

          {/* Team/Values */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-yellow-400/50 transition-all duration-300 hover:scale-105">
              <div className="text-4xl mb-4 group-hover:animate-bounce">🛡️</div>
              <h4 className="text-xl font-bold text-white mb-3 group-hover:text-yellow-300 transition-colors duration-300">
                Güvenlik Öncelikli
              </h4>
              <p className="text-indigo-100 group-hover:text-white transition-colors duration-300">
                Banka seviyesi güvenlik protokolleri ile verilerinizi koruyoruz. 
                BDDK uyumlu ve ISO 27001 sertifikalı güvenlik standartları.
              </p>
            </div>

            <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-green-400/50 transition-all duration-300 hover:scale-105">
              <div className="text-4xl mb-4 group-hover:animate-bounce">🧠</div>
              <h4 className="text-xl font-bold text-white mb-3 group-hover:text-green-300 transition-colors duration-300">
                AI Destekli Zeka
              </h4>
              <p className="text-indigo-100 group-hover:text-white transition-colors duration-300">
                Makine öğrenmesi ve doğal dil işleme teknolojileri ile 
                en akıllı finansal analiz deneyimini sunuyoruz.
              </p>
            </div>

            <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-blue-400/50 transition-all duration-300 hover:scale-105">
              <div className="text-4xl mb-4 group-hover:animate-bounce">🎯</div>
              <h4 className="text-xl font-bold text-white mb-3 group-hover:text-blue-300 transition-colors duration-300">
                Kullanıcı Odaklı
              </h4>
              <p className="text-indigo-100 group-hover:text-white transition-colors duration-300">
                Her özelliği kullanıcı deneyimini merkeze alarak tasarlıyoruz. 
                Feedback'leriniz ürün geliştirme sürecimizin kalbidir.
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
            <Link
              to="/register"
              className="px-10 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-xl font-semibold rounded-xl hover:from-blue-600 hover:to-indigo-700 transform hover:scale-105 transition-all duration-300 shadow-2xl"
            >
              30 Gün Ücretsiz Dene
            </Link>
            <div className="text-blue-200 text-sm">
              ✓ Kredi kartı gerekmez &nbsp;&nbsp; ✓ İstediğiniz zaman iptal edin
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-800 to-slate-900 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-10 right-10 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-10 left-10 w-80 h-80 bg-blue-500/5 rounded-full blur-3xl animate-pulse animation-delay-2000"></div>
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 backdrop-blur-sm px-6 py-3 rounded-full border border-cyan-400/20 mb-8">
              <span className="text-2xl">📞</span>
              <span className="text-white font-semibold">İletişime Geçin</span>
            </div>
            
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                Size Nasıl Yardımcı Olabiliriz?
              </span>
            </h2>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto">
              Sorularınız için 7/24 destek ekibimiz hazır. En kısa sürede size geri dönüş yapacağız.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
            {/* Contact Info */}
            <div className="space-y-8">
              <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-cyan-400/40 transition-all duration-300 hover:scale-105 cursor-pointer">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-full flex items-center justify-center group-hover:animate-bounce">
                    <span className="text-xl">📧</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white group-hover:text-cyan-300 transition-colors duration-300">Email</h4>
                    <p className="text-cyan-200 group-hover:text-white transition-colors duration-300">destek@finoba.ai</p>
                    <p className="text-blue-200 text-sm">24 saat içinde yanıt</p>
                  </div>
                </div>
              </div>

              <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-green-400/40 transition-all duration-300 hover:scale-105 cursor-pointer">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-green-400 to-emerald-600 rounded-full flex items-center justify-center group-hover:animate-bounce">
                    <span className="text-xl">💬</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white group-hover:text-green-300 transition-colors duration-300">Canlı Destek</h4>
                    <p className="text-green-200 group-hover:text-white transition-colors duration-300">Dashboard'dan ulaşın</p>
                    <p className="text-blue-200 text-sm">7/24 online destek</p>
                  </div>
                </div>
              </div>

              <div className="group bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-purple-400/40 transition-all duration-300 hover:scale-105 cursor-pointer">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-pink-600 rounded-full flex items-center justify-center group-hover:animate-bounce">
                    <span className="text-xl">📱</span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white group-hover:text-purple-300 transition-colors duration-300">Sosyal Medya</h4>
                    <p className="text-purple-200 group-hover:text-white transition-colors duration-300">@finobaai</p>
                    <p className="text-blue-200 text-sm">Twitter, LinkedIn, Instagram</p>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-yellow-500/10 to-orange-500/10 backdrop-blur-xl rounded-2xl p-6 border border-yellow-400/20">
                <h4 className="text-lg font-bold text-white mb-3 flex items-center space-x-2">
                  <span>🚀</span>
                  <span>Hızlı Başlayın!</span>
                </h4>
                <p className="text-yellow-100 mb-4">
                  Sorularınızı beklemeden hemen denemeye başlayın. 
                  30 gün ücretsiz, kredi kartı bilgisi gerekmez.
                </p>
                <Link
                  to="/register"
                  className="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-bold rounded-xl hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 hover:scale-105"
                >
                  <span>✨ Hemen Başla</span>
                </Link>
              </div>
            </div>

            {/* Contact Form */}
            <div className="bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold text-white mb-6">📝 Bize Mesaj Gönderin</h3>
              
              <form className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-white font-medium mb-2">Ad Soyad</label>
                    <input
                      type="text"
                      className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-blue-200 focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400/20 transition-all duration-300"
                      placeholder="Adınızı yazın"
                    />
                  </div>
                  <div>
                    <label className="block text-white font-medium mb-2">Email</label>
                    <input
                      type="email"
                      className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-blue-200 focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400/20 transition-all duration-300"
                      placeholder="email@example.com"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-white font-medium mb-2">Konu</label>
                  <select className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400/20 transition-all duration-300">
                    <option value="" className="bg-slate-800">Konu seçin</option>
                    <option value="genel" className="bg-slate-800">Genel Bilgi</option>
                    <option value="teknik" className="bg-slate-800">Teknik Destek</option>
                    <option value="faturalama" className="bg-slate-800">Faturalama</option>
                    <option value="ozellik" className="bg-slate-800">Özellik Talebi</option>
                    <option value="isbirligi" className="bg-slate-800">İş Birliği</option>
                  </select>
                </div>

                <div>
                  <label className="block text-white font-medium mb-2">Mesajınız</label>
                  <textarea
                    rows={5}
                    className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-blue-200 focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400/20 transition-all duration-300 resize-none"
                    placeholder="Mesajınızı buraya yazın..."
                  ></textarea>
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-cyan-500/25 relative overflow-hidden group"
                >
                  <span className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                  <span className="relative flex items-center justify-center space-x-2">
                    <span>📧 Mesaj Gönder</span>
                  </span>
                </button>
              </form>

              <div className="mt-6 p-4 bg-blue-500/10 border border-blue-400/20 rounded-xl">
                <p className="text-blue-100 text-sm text-center">
                  💡 <strong>İpucu:</strong> Teknik sorular için lütfen kullandığınız tarayıcı ve işletim sistemini belirtin.
                </p>
              </div>
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
                <li><a href="#" className="hover:text-white transition-colors">Özellikler</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Güvenlik</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Mobil App</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Destek</h4>
              <ul className="space-y-2 text-blue-100">
                <li><a href="#" className="hover:text-white transition-colors">Yardım Merkezi</a></li>
                <li><a href="#" className="hover:text-white transition-colors">İletişim</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Geri Bildirim</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Durum</a></li>
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

export default LandingPage;
