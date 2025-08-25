# 🚀 Finobai - Akıllı Finans Yönetimi Platformu

Modern, güvenli ve kullanıcı dostu finans yönetimi ve yatırım platformu.

## ✨ Özellikler

### 🎯 Aşama 1 (Tamamlandı)
- ✅ **Modern Tanıtım Sayfası** - Responsive tasarım ile etkileyici landing page
- ✅ **Güvenli Kullanıcı Sistemi** - JWT token tabanlı authentication
- ✅ **API-First Yaklaşım** - RESTful API ile backend-frontend ayrımı
- ✅ **TypeScript Desteği** - Type-safe frontend geliştirme

### 🔮 Gelecek Özellikleri
- 📊 **Bütçe Yönetimi** - Gelir-gider takibi ve kategorilendirme
- 📈 **Borsa Verileri** - Gerçek zamanlı hisse senedi takibi
- 🤖 **AI Tavsiyeleri** - Yapay zeka destekli finansal öneriler

## 🛠️ Teknoloji Stack

### Backend
- **Django 5.2.5** - Python web framework
- **Django REST Framework** - API geliştirme
- **JWT Authentication** - Güvenli token tabanlı kimlik doğrulama
- **CORS Headers** - Frontend-backend iletişimi
- **SQLite** - Geliştirme veritabanı

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type-safe JavaScript
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8+
- Node.js 16+
- npm veya yarn

### 1. Repository'yi Klonlayın
```bash
git clone <repository-url>
cd finoba
```

### 2. Backend Kurulumu
```bash
# Python sanal ortamı aktifleştir
source .venv/bin/activate  # macOS/Linux
# veya
.venv\Scripts\activate     # Windows

# Backend bağımlılıklarını yükle
pip install django djangorestframework django-cors-headers PyJWT python-dotenv

# Veritabanını oluştur
cd backend
python manage.py migrate

# Backend sunucusunu başlat (Port: 8000)
python manage.py runserver
```

### 3. Frontend Kurulumu
```bash
# Yeni terminal açın
cd frontend

# Bağımlılıkları yükle
npm install

# Frontend sunucusunu başlat (Port: 3000)
npm start
```

### 4. Uygulamaya Erişim
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Django Admin:** http://localhost:8000/admin

## 📡 API Endpoints

### Authentication
```
POST /api/auth/register/     # Kullanıcı kaydı
POST /api/auth/login/        # Kullanıcı girişi
POST /api/auth/logout/       # Kullanıcı çıkışı
GET  /api/auth/profile/      # Kullanıcı profili
PATCH /api/auth/profile/update/  # Profil güncelleme
POST /api/auth/refresh/      # Token yenileme
```

## 🎨 Ekran Görüntüleri

### Landing Page
- Modern gradient tasarım
- Özellik kartları
- Call-to-action butonları
- Responsive mobile uyumluluk

### Authentication
- Kullanıcı kaydı formu
- Giriş formu
- Form validasyonları
- Hata mesajları (Türkçe)

### Dashboard
- Kişisel hoş geldin mesajı
- Gelecek özellik önizlemesi
- Hesap bilgileri görüntüleme
- Güvenli çıkış işlemi

## 🔐 Güvenlik Özellikleri

- **JWT Token Authentication** - Güvenli oturum yönetimi
- **CORS Koruması** - Cross-origin isteklerin kontrolü
- **Parola Hashleme** - Django'nun güvenli parola sistemi
- **Token Yenileme** - Otomatik token yenileme mekanizması
- **Form Validasyonları** - Client ve server-side validasyon

## 🧪 Test Kullanıcı Hesabı Oluşturma

```bash
# Backend dizininde
cd backend
python manage.py createsuperuser
```

## 📝 Geliştirme Notları

### Backend Komutları
```bash
python manage.py makemigrations  # Migration dosyalarını oluştur
python manage.py migrate         # Veritabanını güncelle
python manage.py runserver       # Development sunucusunu başlat
```

### Frontend Komutları
```bash
npm start        # Development server
npm run build    # Production build
npm test         # Test runner
```

### Proje Yapısı
```
finoba/
├── backend/                 # Django API backend
│   ├── finoba_api/         # Django proje ayarları
│   │   ├── settings.py     # Ana konfigürasyon
│   │   └── urls.py         # URL routing
│   ├── accounts/           # Kullanıcı yönetimi app
│   │   ├── models.py       # Veri modelleri
│   │   ├── views.py        # API view'ları
│   │   ├── serializers.py  # Data serialization
│   │   ├── authentication.py # JWT auth
│   │   └── utils.py        # Token utilities
│   └── .env                # Environment değişkenleri
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React bileşenleri
│   │   │   ├── auth/       # Authentication sayfaları
│   │   │   ├── LandingPage.tsx
│   │   │   └── Dashboard.tsx
│   │   ├── context/        # React context (AuthContext)
│   │   ├── services/       # API servisleri
│   │   └── index.tsx       # App entry point
│   └── tailwind.config.js  # Tailwind konfigürasyonu
└── .github/
    └── copilot-instructions.md  # GitHub Copilot ayarları
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'e push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

- 💬 Issues sayfasından soru sorabilirsiniz
- 📧 Email: [email@example.com]

---

💡 **Not:** Bu proje aktif geliştirme aşamasındadır. Gelecek güncellemelerde borsa verileri, bütçe yönetimi ve AI tavsiyeleri özellikleri eklenecektir.
