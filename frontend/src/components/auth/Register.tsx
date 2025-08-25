import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.tsx';

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (formData.password !== formData.password_confirm) {
      setError('Parolalar eşleşmiyor');
      return;
    }

    setLoading(true);

    try {
      console.log('Form data being sent:', formData);
      const success = await register(formData);
      if (success) {
        navigate('/dashboard');
      } else {
        setError('Kayıt işlemi başarısız');
      }
    } catch (err: any) {
      console.error('Registration error:', err);
      setError('Bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="relative max-w-md w-full space-y-8">
        <div>
          {/* Logo */}
          <div className="flex justify-center mb-8">
            <Link to="/">
              <img src="/images/finobaai.png" alt="Finobai" className="h-16" />
            </Link>
          </div>
          
          <h2 className="text-center text-3xl font-bold text-white">
            Ücretsiz Hesap Oluşturun
          </h2>
          <p className="mt-2 text-center text-sm text-slate-300">
            Zaten hesabınız var mı?{' '}
            <Link to="/login" className="font-medium text-green-400 hover:text-green-300 transition-colors">
              Giriş Yapın
            </Link>
          </p>
        </div>

        <div className="backdrop-blur-xl bg-white/10 rounded-2xl shadow-2xl border border-white/20 p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="first_name" className="block text-sm font-medium text-slate-200 mb-2">
                  Ad
                </label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  required
                  value={formData.first_name}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                  placeholder="Adınız"
                />
              </div>
              
              <div>
                <label htmlFor="last_name" className="block text-sm font-medium text-slate-200 mb-2">
                  Soyad
                </label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  required
                  value={formData.last_name}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                  placeholder="Soyadınız"
                />
              </div>
            </div>

            <div>
              <label htmlFor="username" className="block text-sm font-medium text-slate-200 mb-2">
                Kullanıcı Adı
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                placeholder="Kullanıcı adınız"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-200 mb-2">
                E-posta Adresi
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                placeholder="ornek@email.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-200 mb-2">
                Şifre
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                placeholder="••••••••"
              />
            </div>

            <div>
              <label htmlFor="password_confirm" className="block text-sm font-medium text-slate-200 mb-2">
                Şifre Tekrarı
              </label>
              <input
                id="password_confirm"
                name="password_confirm"
                type="password"
                required
                value={formData.password_confirm}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div className="bg-red-500/20 border border-red-500/30 rounded-xl p-3">
                <p className="text-sm text-red-200">{error}</p>
              </div>
            )}

            <div className="flex items-center">
              <input
                id="terms"
                name="terms"
                type="checkbox"
                required
                className="h-4 w-4 bg-white/10 border-white/20 rounded focus:ring-green-500 text-green-600"
              />
              <label htmlFor="terms" className="ml-2 block text-sm text-slate-300">
                <button type="button" className="text-green-400 hover:text-green-300 transition-colors">Kullanım Şartları</button>'nı ve{' '}
                <button type="button" className="text-green-400 hover:text-green-300 transition-colors">Gizlilik Politikası</button>'nı kabul ediyorum
              </label>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-300 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Hesap oluşturuluyor...' : '🚀 Ücretsiz Hesap Oluştur'}
              </button>
            </div>
          </form>
        </div>

        {/* Back to Home */}
        <div className="text-center">
          <Link to="/" className="text-slate-400 hover:text-white transition-colors text-sm">
            ← Anasayfaya Dön
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
