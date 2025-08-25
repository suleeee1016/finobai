<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Finobai - Finans Yönetimi Platformu

Bu proje, modern bir finans yönetimi ve yatırım platformudur. Aşağıdaki teknolojiler ve kurallar kullanılmaktadır:

## Teknoloji Stack

### Backend
- Django 5.2.5 - Python web framework
- Django REST Framework - API geliştirme
- JWT Authentication - Token tabanlı kimlik doğrulama
- CORS Headers - Frontend-backend iletişimi
- SQLite - Geliştirme veritabanı

### Frontend
- React 18 with TypeScript - Modern UI framework
- React Router Dom - Client-side routing
- Axios - HTTP client
- Tailwind CSS - Utility-first CSS framework

## Proje Yapısı

```
finoba/
├── backend/                 # Django API backend
│   ├── finoba_api/         # Django proje ayarları
│   ├── accounts/           # Kullanıcı yönetimi uygulaması
│   └── manage.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React bileşenleri
│   │   ├── context/        # React context (AuthContext)
│   │   └── services/       # API servisleri
│   └── public/
└── .venv/                 # Python sanal ortamı
```

## Önemli Kurallar

1. **Authentication**: JWT token tabanlı authentication kullanılır
2. **API Endpoints**: Tüm API endpoint'leri `/api/` prefix'i ile başlar
3. **CORS**: Frontend `http://localhost:3000` adresinden backend'e erişir
4. **TypeScript**: Frontend'de strict TypeScript kullanılır
5. **Tailwind CSS**: Styling için Tailwind CSS kullanılır
6. **Türkçe**: UI ve hata mesajları Türkçe olmalıdır

## API Endpoints

- `POST /api/auth/register/` - Kullanıcı kaydı
- `POST /api/auth/login/` - Kullanıcı girişi
- `POST /api/auth/logout/` - Kullanıcı çıkışı
- `GET /api/auth/profile/` - Kullanıcı profili
- `PATCH /api/auth/profile/update/` - Profil güncelleme
- `POST /api/auth/refresh/` - Token yenileme

## Geliştirme Notları

- Backend: `cd backend && python manage.py runserver`
- Frontend: `cd frontend && npm start`
- Migrations: `cd backend && python manage.py makemigrations && python manage.py migrate`

Bu platform gelecekte borsa verileri, bütçe yönetimi ve AI tavsiyeleri özellikleri ile genişletilecektir.
