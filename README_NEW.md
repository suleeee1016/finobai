# 🚀 Finobai - Akıllı Finans Yönetimi Platformu

> Modern, güvenli ve AI destekli finans yönetimi ve yatırım platformu

<div align="center">
  
  ![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
  ![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)
  ![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
  ![TypeScript](https://img.shields.io/badge/TypeScript-4.7.4-blue.svg)
  ![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

## 📖 İçindekiler
- [🎯 Özellikler](#-özellikler)
- [🏗️ Sistem Mimarisi](#️-sistem-mimarisi)
- [🛠️ Teknoloji Stack](#️-teknoloji-stack)
- [🚀 Kurulum ve Çalıştırma](#-kurulum-ve-çalıştırma)
- [📡 API Referansı](#-api-referansı)
- [🚦 Deployment](#-deployment)
- [🧪 Test](#-test)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)

## 🎯 Özellikler

### ✅ Mevcut Özellikler
| Özellik | Durum | Açıklama |
|---------|--------|----------|
| 👤 **Kullanıcı Yönetimi** | ✅ | JWT tabanlı authentication, kayıt/giriş/profil yönetimi |
| 💰 **Gider Takibi** | ✅ | Kişisel harcama analizi, kategorizasyon ve raporlama |
| 🎯 **Hedef Takibi** | ✅ | Finansal hedefler belirleme ve ilerleme takibi |
| 📈 **Borsa Analizi** | ✅ | Hisse senedi verileri, teknik analiz ve AI önerileri |
| 🤖 **AI Servisleri** | ✅ | OpenAI entegrasyonu ile akıllı finansal tavsiyeler |
| 📱 **Responsive UI** | ✅ | Modern, mobil uyumlu React/TypeScript arayüzü |

### 🚀 Gelecek Özellikler
- 📊 **Gelişmiş Analytics**: Detaylı finansal raporlar ve görselleştirmeler
- 🏦 **Banka Entegrasyonu**: Otomatik hesap senkronizasyonu
- 💳 **Kredi Kartı Analizi**: Harcama trendleri ve limit optimizasyonu  
- 🌍 **Multi-Currency**: Çoklu para birimi desteği
- 📧 **Bildirim Sistemi**: E-posta ve push notification'lar
- 🔐 **2FA Güvenlik**: İki faktörlü kimlik doğrulama

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   External      │
│                 │    │                  │    │   Services      │
│ React + TS      │────│ Django + DRF     │────│ OpenAI API      │
│ Tailwind CSS    │    │ JWT Auth         │    │ Stock APIs      │
│ Axios Client    │    │ PostgreSQL       │    │ Bank APIs       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Mikroservis Yapısı:**
- **accounts**: Kullanıcı yönetimi ve authentication
- **expense_tracker**: Gider takibi ve kategorizasyon
- **goal_tracker**: Finansal hedef yönetimi
- **stock_market**: Borsa verileri ve analiz
- **ai_services**: AI destekli tavsiye sistemi

## 🛠️ Teknoloji Stack

### 🔧 Backend (Django)
```python
# Core Framework
Django==5.2.5                    # Web framework
djangorestframework>=3.14.0      # API framework
django-cors-headers>=4.0.0       # CORS middleware

# Authentication & Security  
PyJWT>=2.8.0                     # JWT token handling
python-dotenv>=1.0.0             # Environment variables
cryptography>=41.0.0             # Encryption utilities

# Database & Storage
psycopg2-binary>=2.9.0          # PostgreSQL adapter
dj-database-url>=2.0.0          # Database URL parsing

# AI & External APIs
openai>=1.3.0                   # OpenAI integration
requests>=2.31.0                # HTTP requests
```

### ⚛️ Frontend (React + TypeScript)
```json
{
  "react": "^18.2.0",           // Core React framework
  "typescript": "^4.7.4",       // TypeScript support
  "react-router-dom": "^6.30.1", // Client-side routing
  "axios": "^1.4.0",            // HTTP client
  "tailwindcss": "^3.3.0"       // Utility-first CSS
}
```

### 🗄️ Veritabanı Şeması
```sql
-- Kullanıcı tabloları
User (Django built-in)
├── UserProfile (1:1)
└── UserPreferences (1:1)

-- Finansal veri tabloları  
FinancialGoal (1:N User)
├── GoalContribution (N:1)
├── GoalMilestone (N:1)
└── GoalReminder (N:1)

ExpenseCategory (N:N User)
└── Expense (N:1 User, N:1 Category)

StockData (Global)
└── UserPortfolio (N:1 User, N:1 Stock)
```

## 🚀 Kurulum ve Çalıştırma

### 📋 Gereksinimler
- **Python**: 3.8+ (önerilen: 3.11+)
- **Node.js**: 16+ (önerilen: 18+)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **OS**: macOS, Linux, Windows

### 🔧 Yerel Geliştirme Ortamı

#### 1️⃣ Repository'yi İndirin
```bash
git clone https://github.com/username/finoba.git
cd finoba
```

#### 2️⃣ Backend Kurulumu
```bash
# Virtual environment oluştur ve aktifleştir
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Dependencies yükle
cd backend
pip install -r requirements_production.txt

# Environment variables
cp .env.example .env
# .env dosyasını düzenleyerek API anahtarlarını ekleyin

# Database migration
python manage.py makemigrations
python manage.py migrate

# Superuser oluştur
python manage.py createsuperuser

# Development server başlat
python manage.py runserver
```

#### 3️⃣ Frontend Kurulumu
```bash
# Yeni terminal açın
cd frontend

# Dependencies yükle
npm install

# Development server başlat  
npm start
```

#### 4️⃣ Erişim URL'leri
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000/api
- 👑 **Django Admin**: http://localhost:8000/admin

### 🌍 Environment Variables

#### Backend (.env)
```bash
# Django Core
SECRET_KEY=your-super-secret-django-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database (Production)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# AI Services
OPENAI_API_KEY=sk-proj-your-openai-api-key-here

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days in minutes
```

#### Frontend (.env.local)
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api

# Feature Flags
REACT_APP_ENABLE_AI_FEATURES=true
REACT_APP_ENABLE_STOCK_ANALYSIS=true
REACT_APP_ENABLE_BANK_SYNC=false

# Analytics (Production)
REACT_APP_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
```

## 📡 API Referansı

### 🔐 Authentication Endpoints

| Method | Endpoint | Açıklama | Payload |
|--------|----------|----------|---------|
| `POST` | `/api/auth/register/` | Kullanıcı kaydı | `{username, email, password, password_confirm, first_name, last_name}` |
| `POST` | `/api/auth/login/` | Kullanıcı girişi | `{email, password}` |
| `POST` | `/api/auth/logout/` | Kullanıcı çıkışı | `{refresh_token}` |
| `GET` | `/api/auth/profile/` | Profil bilgisi | - |
| `PATCH` | `/api/auth/profile/update/` | Profil güncelle | `{first_name?, last_name?, email?}` |
| `POST` | `/api/auth/refresh/` | Token yenile | `{refresh_token}` |

### 💰 Expense Tracking

| Method | Endpoint | Açıklama | Payload |
|--------|----------|----------|---------|
| `GET` | `/api/expenses/` | Gider listesi | - |
| `POST` | `/api/expenses/` | Yeni gider | `{amount, category, description, date}` |
| `GET` | `/api/expenses/categories/` | Kategori listesi | - |
| `GET` | `/api/expenses/analytics/` | Harcama analizi | `?period=monthly&year=2024` |

### 🎯 Goal Tracking

| Method | Endpoint | Açıklama | Payload |
|--------|----------|----------|---------|
| `GET` | `/api/goals/` | Hedef listesi | - |
| `POST` | `/api/goals/` | Yeni hedef | `{name, target_amount, target_date, category}` |
| `POST` | `/api/goals/{id}/contribute/` | Katkı ekle | `{amount, note?}` |
| `GET` | `/api/goals/analytics/` | Hedef analizi | - |

### 📈 Stock Market

| Method | Endpoint | Açıklama | Payload |
|--------|----------|----------|---------|
| `GET` | `/api/stocks/search/` | Hisse arama | `?q=AAPL` |
| `GET` | `/api/stocks/{symbol}/` | Hisse detayı | - |
| `POST` | `/api/stocks/analyze/` | AI analiz | `{symbols: ['AAPL', 'GOOGL']}` |
| `GET` | `/api/stocks/portfolio/` | Kullanıcı portföyü | - |

### 🤖 AI Services

| Method | Endpoint | Açıklama | Payload |
|--------|----------|----------|---------|
| `POST` | `/api/ai/financial-advice/` | Finansal tavsiye | `{context, question}` |
| `POST` | `/api/ai/budget-analysis/` | Bütçe analizi | `{income, expenses, goals}` |
| `POST` | `/api/ai/investment-recommendation/` | Yatırım önerisi | `{risk_profile, budget, timeline}` |

### 📊 Response Format

#### Başarılı Response
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Example Data",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "İşlem başarıyla tamamlandı"
}
```

#### Hata Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Gerekli alanlar eksik",
    "details": {
      "email": ["Bu alan zorunludur"],
      "password": ["Minimum 8 karakter olmalıdır"]
    }
  }
}
```

## 🚦 Deployment

### 🌐 Production Deployment Seçenekleri

#### Option 1: Railway + Vercel (Önerilen)
```bash
# 1. Railway Backend Deploy
railway login
railway new
railway add postgresql
railway deploy

# 2. Vercel Frontend Deploy  
vercel --prod
```

#### Option 2: VDS/Docker Deployment
```bash
# VDS manager scripti ile otomatik deployment
./vds_manager.sh deploy --server=your-server-ip

# Manuel Docker deployment
docker-compose up --build -d
```

### 🔧 Production Ayarları

#### Backend Production Settings
```python
# settings_production.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', '*.railway.app']

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
```

#### Frontend Build Configuration
```json
{
  "scripts": {
    "build": "react-scripts build",
    "build:prod": "NODE_ENV=production npm run build"
  },
  "homepage": "https://yourdomain.com"
}
```

### 📈 Monitoring & Logging

#### Health Check Endpoints
- `GET /api/health/` - API sağlık kontrolü
- `GET /api/health/db/` - Veritabanı bağlantı kontrolü
- `GET /api/health/ai/` - AI servis durumu

#### Log Management
```python
# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'finoba.log',
        },
    },
    'loggers': {
        'finoba': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🧪 Test

### Backend Testleri
```bash
cd backend

# Tüm testleri çalıştır
python manage.py test

# Belirli app testleri
python manage.py test accounts
python manage.py test goal_tracker

# Coverage raporu
coverage run --source='.' manage.py test
coverage report
coverage html  # HTML rapor
```

### Frontend Testleri
```bash
cd frontend

# Unit testler
npm test

# E2E testler (gelecek)
npm run test:e2e

# Test coverage
npm test -- --coverage
```

### API Test Collection
Postman koleksiyonu: `docs/Finobai_API_Collection.json`

```bash
# Newman ile otomatik test
newman run docs/Finobai_API_Collection.json \
  --environment docs/test_environment.json
```

## 📊 Performans

### Backend Optimizasyonları
- **Database**: Query optimization, indexing
- **Caching**: Redis cache layer (gelecek)
- **API**: Pagination, field selection
- **Static Files**: CDN integration (prod)

### Frontend Optimizasyonları  
- **Bundle Size**: Code splitting, lazy loading
- **Performance**: React.memo, useMemo optimizations
- **Assets**: Image compression, WebP format
- **Caching**: Service worker (gelecek)

## 🔐 Güvenlik

### Mevcut Güvenlik Özellikleri
- ✅ JWT token tabanlı authentication
- ✅ Password validation (minimum 8 karakter)
- ✅ CORS configuration
- ✅ SQL injection koruması (Django ORM)
- ✅ XSS koruması (Django built-in)
- ✅ HTTPS enforcement (production)

### Gelecek Güvenlik Özellikleri
- 🔐 2FA (Two-Factor Authentication)
- 🛡️ Rate limiting
- 🔒 API key rotation
- 🚫 Fraud detection
- 📧 Security notifications

## 🤝 Katkıda Bulunma

### Development Workflow
1. **Fork** repository'yi fork edin
2. **Branch** yeni feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. **Code** kodunuzu yazın ve test edin
4. **Commit** değişiklikleri commit edin (`git commit -m 'feat: add amazing feature'`)
5. **Push** branch'inizi push edin (`git push origin feature/amazing-feature`)
6. **PR** Pull Request oluşturun

### Code Style Guide

#### Python (Backend)
```python
# PEP 8 standardları
# Black formatter kullanın
# Type hints zorunlu

def create_financial_goal(
    user: User, 
    name: str, 
    target_amount: Decimal
) -> FinancialGoal:
    """Yeni finansal hedef oluştur."""
    pass
```

#### TypeScript (Frontend)
```typescript
// Prettier + ESLint
// Strict TypeScript

interface FinancialGoal {
  id: number;
  name: string;
  targetAmount: number;
  currentAmount: number;
  targetDate: string;
}

const createGoal = async (goalData: CreateGoalRequest): Promise<FinancialGoal> => {
  // Implementation
};
```

### Git Commit Convention
```
feat: yeni özellik eklendi
fix: bug düzeltildi  
docs: dokümantasyon güncellendi
style: code style değişiklikleri
refactor: kod refactor edildi
test: test eklendi/güncellendi
chore: build/config değişiklikleri
```

## 📚 Dokümantasyon

### API Dokümantasyonu
- **Swagger/OpenAPI**: `/api/docs/` (geliştirme aşamasında)
- **Postman Collection**: `docs/api/Finobai_Collection.json`
- **GraphQL Schema**: Gelecek sürümlerde

### Architecture Decision Records (ADR)
- [ADR-001: Technology Stack Selection](docs/adr/001-tech-stack.md)
- [ADR-002: Authentication Strategy](docs/adr/002-auth-strategy.md)
- [ADR-003: Database Design](docs/adr/003-database-design.md)

### Deployment Guides
- [🚀 Railway Deployment](docs/deployment/railway.md)
- [🌐 VDS Deployment](VDS_DEPLOYMENT_GUIDE.md)
- [🐳 Docker Deployment](docs/deployment/docker.md)

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

## 📞 İletişim & Destek

### Geliştirici İletişim
- **Email**: sumeyyesahin@example.com
- **GitHub**: [@sumeyyesahin](https://github.com/sumeyyesahin)
- **LinkedIn**: [Sümeyye Şahin](https://linkedin.com/in/sumeyyesahin)

### Destek & Bilgilendirme
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/username/finoba/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/username/finoba/discussions)
- 📖 **Wiki**: [Project Wiki](https://github.com/username/finoba/wiki)

---

<div align="center">

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

Made with ❤️ by [Finobai Team](https://github.com/username/finoba)

</div>
