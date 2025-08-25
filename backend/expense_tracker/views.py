from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from datetime import datetime, timedelta
import json
import csv
import io
import re

from .models import Expense, ExpenseCategory, Budget, ExpenseInsight, CreditCardStatement, StatementTransaction
from .services import ExpenseAnalysisService


@method_decorator(csrf_exempt, name='dispatch')
class ExpenseAnalysisView(APIView):
    """Harcama analizi endpoint'i"""
    permission_classes = [AllowAny]  # Geçici
    
    def post(self, request):
        """Harcama metnini analiz et"""
        try:
            expense_text = request.data.get('expense_text', '').strip()
            amount = float(request.data.get('amount', 0))
            
            if not expense_text or amount <= 0:
                return Response({
                    'error': 'Harcama açıklaması ve geçerli bir tutar gerekli'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # AI analiz servisi
            analysis_service = ExpenseAnalysisService()
            analysis = analysis_service.analyze_expense_text(expense_text, amount)
            
            # Kategori bilgisini ekle
            try:
                category = ExpenseCategory.objects.get(name=analysis['category'])
                analysis['category_info'] = {
                    'name': category.get_name_display(),
                    'icon': category.icon,
                    'color': category.color
                }
            except ExpenseCategory.DoesNotExist:
                # Kategori bulunamazsa, mapping ile dene
                category_mapping = {
                    'food': ('🍽️', 'Gıda & İçecek', '#ef4444'),
                    'transport': ('🚗', 'Ulaşım', '#3b82f6'),
                    'entertainment': ('🎬', 'Eğlence', '#8b5cf6'),
                    'bills': ('�', 'Faturalar', '#f59e0b'),
                    'shopping': ('🛍️', 'Alışveriş', '#ec4899'),
                    'health': ('🏥', 'Sağlık', '#10b981'),
                    'education': ('�', 'Eğitim', '#06b6d4'),
                    'investment': ('📈', 'Yatırım', '#84cc16'),
                    'housing': ('🏠', 'Konut', '#f97316'),
                    'other': ('📦', 'Diğer', '#6366f1')
                }
                
                cat_data = category_mapping.get(analysis['category'], category_mapping['other'])
                analysis['category_info'] = {
                    'name': cat_data[1],
                    'icon': cat_data[0],
                    'color': cat_data[2]
                }
            
            return Response({
                'analysis': analysis,
                'suggestion': f"Bu harcamanız {analysis['category_info']['name']} kategorisine uygun görünüyor. Güven oranı: %{analysis['confidence']*100:.0f}"
            })
            
        except Exception as e:
            print(f"Expense analysis error: {e}")
            return Response({
                'error': 'Harcama analizi yapılırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch') 
class MonthlySummaryView(APIView):
    """Aylık harcama özeti"""
    permission_classes = [AllowAny]  # Geçici
    
    def get(self, request):
        """Aylık özet getir"""
        try:
            now = datetime.now()
            month = int(request.GET.get('month', now.month))
            year = int(request.GET.get('year', now.year))
            
            # Gerçek ekstre verilerini al
            real_summary = self._get_real_monthly_summary(month, year)
            
            if real_summary:
                return Response(real_summary)
            
            # Eğer gerçek veri yoksa mock veri kullan
            mock_summary = {
                'total_spent': 12450.75,
                'expense_count': 47,
                'category_summary': {
                    'food': {
                        'amount': 3200.50,
                        'count': 15,
                        'icon': '🍽️',
                        'color': '#ef4444',
                        'name': 'Gıda & İçecek',
                        'percentage': 25.7
                    },
                    'transport': {
                        'amount': 2100.25,
                        'count': 8,
                        'icon': '🚗',
                        'color': '#3b82f6',
                        'name': 'Ulaşım',
                        'percentage': 16.9
                    },
                    'entertainment': {
                        'amount': 1800.00,
                        'count': 6,
                        'icon': '🎬',
                        'color': '#8b5cf6',
                        'name': 'Eğlence',
                        'percentage': 14.5
                    },
                    'bills': {
                        'amount': 2650.00,
                        'count': 4,
                        'icon': '💡',
                        'color': '#f59e0b',
                        'name': 'Faturalar',
                        'percentage': 21.3
                    },
                    'shopping': {
                        'amount': 1900.00,
                        'count': 10,
                        'icon': '🛍️',
                        'color': '#ec4899',
                        'name': 'Alışveriş',
                        'percentage': 15.3
                    },
                    'other': {
                        'amount': 800.00,
                        'count': 4,
                        'icon': '📦',
                        'color': '#6366f1',
                        'name': 'Diğer',
                        'percentage': 6.4
                    }
                },
                'top_category': 'food',
                'top_category_amount': 3200.50,
                'average_per_day': 415.02,
                'month': month,
                'year': year,
                'insights': [
                    {
                        'type': 'warning',
                        'icon': '⚠️',
                        'title': 'Gıda Bütçesi Uyarısı',
                        'message': 'Bu ay gıda harcamalarınız planladığınızdan %15 fazla. Dışarıda yemek yeme sıklığınızı azaltmayı düşünebilirsiniz.',
                        'priority': 4
                    },
                    {
                        'type': 'suggestion',
                        'icon': '💡',
                        'title': 'Tasarruf Fırsatı',
                        'message': 'Ulaşım harcamalarınızı azaltmak için toplu taşıma aboneliği düşünebilirsiniz. Aylık 300₺ tasarruf sağlayabilir.',
                        'priority': 3
                    },
                    {
                        'type': 'achievement',
                        'icon': '🎉',
                        'title': 'Tebrikler!',
                        'message': 'Bu ay faturalarınızı zamanında ödemeyi başardınız. Kredi notunuza olumlu katkı sağladı.',
                        'priority': 2
                    }
                ]
            }
            
            return Response(mock_summary)
            
        except Exception as e:
            print(f"Monthly summary error: {e}")
            return Response({
                'error': 'Aylık özet alınırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_real_monthly_summary(self, month, year):
        """Gerçek ekstre verilerinden aylık özet oluştur"""
        try:
            from datetime import datetime, date
            from collections import defaultdict
            
            # Belirtilen ay için ekstreleri filtrele
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)
            
            # Bu aya ait işlemleri bul
            transactions = StatementTransaction.objects.filter(
                date__gte=start_date,
                date__lt=end_date
            ).select_related('statement')
            
            if not transactions.exists():
                return None
            
            # Kategori toplamları
            category_totals = defaultdict(lambda: {'amount': 0, 'count': 0})
            total_amount = 0
            transaction_count = transactions.count()
            
            for transaction in transactions:
                category = transaction.category
                amount = float(transaction.amount)
                
                category_totals[category]['amount'] += amount
                category_totals[category]['count'] += 1
                total_amount += amount
            
            # Kategori bilgilerini zenginleştir
            category_mapping = {
                'food': ('🍽️', 'Gıda & İçecek', '#ef4444'),
                'transport': ('🚗', 'Ulaşım', '#3b82f6'),
                'entertainment': ('🎬', 'Eğlence', '#8b5cf6'),
                'bills': ('💡', 'Faturalar', '#f59e0b'),
                'shopping': ('🛍️', 'Alışveriş', '#ec4899'),
                'health': ('🏥', 'Sağlık', '#10b981'),
                'education': ('📚', 'Eğitim', '#06b6d4'),
                'investment': ('📈', 'Yatırım', '#84cc16'),
                'housing': ('🏠', 'Konut', '#f97316'),
                'other': ('📦', 'Diğer', '#6366f1')
            }
            
            category_summary = {}
            for category, data in category_totals.items():
                icon, name, color = category_mapping.get(category, category_mapping['other'])
                percentage = (data['amount'] / total_amount) * 100 if total_amount > 0 else 0
                
                category_summary[category] = {
                    'amount': data['amount'],
                    'count': data['count'],
                    'icon': icon,
                    'color': color,
                    'name': name,
                    'percentage': round(percentage, 1)
                }
            
            # En büyük kategoriyi bul
            top_category = max(category_summary.items(), key=lambda x: x[1]['amount']) if category_summary else None
            top_category_name = top_category[0] if top_category else 'other'
            top_category_amount = top_category[1]['amount'] if top_category else 0
            
            # Günlük ortalama
            from calendar import monthrange
            days_in_month = monthrange(year, month)[1]
            average_per_day = total_amount / days_in_month
            
            # Gerçek verilerden insights oluştur
            insights = self._generate_monthly_insights(category_summary, total_amount, transaction_count)
            
            return {
                'total_spent': total_amount,
                'expense_count': transaction_count,
                'category_summary': category_summary,
                'top_category': top_category_name,
                'top_category_amount': top_category_amount,
                'average_per_day': average_per_day,
                'month': month,
                'year': year,
                'insights': insights,
                'data_source': 'real_statements'  # Gerçek veri olduğunu belirt
            }
            
        except Exception as e:
            print(f"Real monthly summary error: {e}")
            return None
    
    def _generate_monthly_insights(self, category_summary, total_amount, transaction_count):
        """Aylık verilerden insights oluştur"""
        insights = []
        
        try:
            if not category_summary:
                return insights
            
            # En yüksek harcama kategorisi
            top_category = max(category_summary.items(), key=lambda x: x[1]['amount'])
            top_cat_name = top_category[1]['name']
            top_cat_percentage = top_category[1]['percentage']
            top_cat_amount = top_category[1]['amount']
            
            if top_cat_percentage > 40:
                insights.append({
                    'type': 'warning',
                    'icon': '⚠️',
                    'title': f'{top_cat_name} Ağırlıklı Ay',
                    'message': f'Bu ay harcamalarınızın %{top_cat_percentage}\'i {top_cat_name} kategorisinde. Dengeyi gözden geçirebilirsiniz.',
                    'priority': 4
                })
            elif top_cat_percentage > 25:
                insights.append({
                    'type': 'info',
                    'icon': '💡',
                    'title': f'{top_cat_name} Odaklı Ay',
                    'message': f'{top_cat_name} harcamalarınız bu ay toplam bütçenizin %{top_cat_percentage}\'ini oluşturdu.',
                    'priority': 2
                })
            
            # Ortalama işlem analizi
            avg_transaction = total_amount / transaction_count if transaction_count > 0 else 0
            if avg_transaction > 500:
                insights.append({
                    'type': 'suggestion',
                    'icon': '📊',
                    'title': 'Yüksek Ortalama Harcama',
                    'message': f'Bu ay ortalama işlem tutarınız ₺{avg_transaction:.2f}. Küçük harcamaları da takip etmeyi düşünün.',
                    'priority': 3
                })
            
            # Toplam harcama değerlendirmesi
            if total_amount > 15000:
                insights.append({
                    'type': 'warning',
                    'icon': '💸',
                    'title': 'Yüksek Aylık Harcama',
                    'message': f'Bu ay toplam ₺{total_amount:.2f} harcama yaptınız. Bütçe planınızı gözden geçirebilirsiniz.',
                    'priority': 4
                })
            elif total_amount < 5000:
                insights.append({
                    'type': 'achievement',
                    'icon': '🎉',
                    'title': 'Tasarruflu Ay',
                    'message': f'Bu ay sadece ₺{total_amount:.2f} harcama yaptınız. Harika bir tasarruf performansı!',
                    'priority': 1
                })
            
            # İşlem sayısı analizi
            if transaction_count > 50:
                insights.append({
                    'type': 'info',
                    'icon': '📈',
                    'title': 'Aktif Harcama Dönemi',
                    'message': f'Bu ay {transaction_count} işlem gerçekleştirdiniz. Harcama alışkanlıklarınızı analiz edebilirsiniz.',
                    'priority': 2
                })
            
            # Genel başarı mesajı
            if len(insights) < 2:
                insights.append({
                    'type': 'achievement',
                    'icon': '✅',
                    'title': 'Analiz Tamamlandı',
                    'message': f'Bu ay {transaction_count} işleminiz analiz edildi. Finansal durumunuz kontrol altında görünüyor.',
                    'priority': 1
                })
            
            return insights[:5]  # En fazla 5 insight
            
        except Exception as e:
            print(f"Monthly insights error: {e}")
            return [{
                'type': 'info',
                'icon': '📊',
                'title': 'Aylık Analiz',
                'message': 'Verileriniz başarıyla analiz edildi.',
                'priority': 1
            }]


@method_decorator(csrf_exempt, name='dispatch')
class ExpenseCategoriesView(APIView):
    """Harcama kategorileri listesi"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Tüm kategorileri getir"""
        try:
            categories = []
            category_data = [
                ('food', '🍽️', '#ef4444', 'Gıda & İçecek'),
                ('transport', '🚗', '#3b82f6', 'Ulaşım'),
                ('entertainment', '🎬', '#8b5cf6', 'Eğlence'),
                ('bills', '💡', '#f59e0b', 'Faturalar'),
                ('shopping', '🛍️', '#ec4899', 'Alışveriş'),
                ('health', '🏥', '#10b981', 'Sağlık'),
                ('education', '📚', '#06b6d4', 'Eğitim'),
                ('investment', '📈', '#84cc16', 'Yatırım'),
                ('housing', '🏠', '#f97316', 'Konut'),
                ('other', '📦', '#6366f1', 'Diğer')
            ]
            
            for code, icon, color, name in category_data:
                categories.append({
                    'code': code,
                    'name': name,
                    'icon': icon,
                    'color': color
                })
            
            return Response({'categories': categories})
            
        except Exception as e:
            print(f"Categories error: {e}")
            return Response({
                'error': 'Kategoriler alınırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CreditCardStatementUploadView(APIView):
    """Kredi kartı ekstresi yükleme ve analiz endpoint'i"""
    permission_classes = [AllowAny]  # Geçici
    
    def post(self, request):
        """Kredi kartı ekstresini yükle ve analiz et"""
        try:
            # Dosya kontrolü
            if 'file' not in request.FILES:
                return Response({
                    'error': 'Ekstre dosyası gerekli'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            file = request.FILES['file']
            
            # Dosya tipi kontrolü
            if not file.name.lower().endswith(('.csv', '.txt', '.xlsx')):
                return Response({
                    'error': 'Sadece CSV, TXT veya XLSX formatları destekleniyor'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Dosya boyutu kontrolü (5MB max)
            if file.size > 5 * 1024 * 1024:
                return Response({
                    'error': 'Dosya boyutu 5MB\'dan küçük olmalı'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Dosyayı oku ve parse et
            try:
                if file.name.lower().endswith('.csv'):
                    transactions = self._parse_csv_statement(file)
                elif file.name.lower().endswith('.txt'):
                    transactions = self._parse_txt_statement(file)
                else:
                    return Response({
                        'error': 'Bu dosya formatı henüz desteklenmiyor'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not transactions:
                    return Response({
                        'error': 'Dosyada geçerli işlem bulunamadı'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # AI analizi yap
                analysis = self._analyze_credit_card_statement(transactions)
                
                # Ekstreyi veritabanına kaydet
                statement = self._save_statement_to_db(file.name, analysis, transactions)
                
                return Response({
                    'success': True,
                    'analysis': analysis,
                    'transaction_count': len(transactions),
                    'file_name': file.name,
                    'statement_id': statement.id if statement else None
                })
                
            except Exception as parse_error:
                print(f"Parse error: {parse_error}")
                return Response({
                    'error': f'Dosya ayrıştırılırken hata oluştu: {str(parse_error)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(f"Credit card statement upload error: {e}")
            return Response({
                'error': 'Ekstre analizi yapılırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _parse_csv_statement(self, file):
        """CSV formatındaki ekstre dosyasını parse et"""
        transactions = []
        try:
            # Dosyayı string olarak oku
            content = file.read().decode('utf-8-sig')
            csv_reader = csv.reader(io.StringIO(content))
            
            # Header'ı oku
            header = next(csv_reader, None)
            print(f"CSV Header: {header}")
            
            if not header:
                return []
            
            # Header sütunlarının indekslerini bul
            date_col = -1
            desc_col = -1  
            amount_col = -1
            type_col = -1
            
            # Yaygın sütun adlarını ara
            header_lower = [col.lower() for col in header]
            
            # Tarih sütunu
            for i, col in enumerate(header_lower):
                if any(keyword in col for keyword in ['tarih', 'date', 'islem_tarihi']):
                    date_col = i
                    break
            
            # Açıklama sütunu
            for i, col in enumerate(header_lower):
                if any(keyword in col for keyword in ['aciklama', 'açıklama', 'description', 'desc', 'merchant', 'is_yeri']):
                    desc_col = i
                    break
            
            # Tutar sütunu
            for i, col in enumerate(header_lower):
                if any(keyword in col for keyword in ['tutar', 'amount', 'miktar']):
                    amount_col = i
                    break
            
            # İşlem tipi sütunu
            for i, col in enumerate(header_lower):
                if any(keyword in col for keyword in ['islem_tipi', 'tip', 'type']):
                    type_col = i
                    break
            
            print(f"Column mapping - Date: {date_col}, Desc: {desc_col}, Amount: {amount_col}, Type: {type_col}")
            
            # Fallback: eğer sütun bulunamazsa varsayılan pozisyonları kullan
            if date_col == -1:
                date_col = 0
            if desc_col == -1:
                desc_col = 2 if len(header) > 2 else 1
            if amount_col == -1:
                amount_col = 5 if len(header) > 5 else (len(header) - 1)
            
            row_count = 0
            for row in csv_reader:
                row_count += 1
                print(f"Processing row {row_count}: {row}")
                
                if len(row) <= max(date_col, desc_col, amount_col):
                    print(f"Skipping row {row_count}: not enough columns")
                    continue
                
                # Sütunlardan veriyi çıkar
                date_str = row[date_col].strip() if date_col < len(row) and row[date_col] else ''
                
                # Açıklama için birden fazla sütunu birleştir
                if desc_col < len(row):
                    description = row[desc_col].strip()
                    # İş yeri bilgisi varsa ekle
                    if len(row) > 12 and row[12].strip():  # is_yeri sütunu
                        description = f"{row[12].strip()} - {description}"
                else:
                    description = ''
                
                amount_str = row[amount_col].strip() if amount_col < len(row) and row[amount_col] else '0'
                
                # İşlem tipini kontrol et (ödeme, iade vs. harcama olmayan işlemleri filtrele)
                transaction_type = ''
                if type_col != -1 and type_col < len(row):
                    transaction_type = row[type_col].strip().lower()
                
                print(f"Parsed data: date={date_str}, desc={description}, amount={amount_str}, type={transaction_type}")
                
                # Harcama olmayan işlemleri filtrele
                if transaction_type in ['ödeme', 'iade', 'faiz', 'ucret']:
                    print(f"Skipping non-expense transaction: {transaction_type}")
                    continue
                
                # Tarih parse et
                try:
                    # Çeşitli tarih formatlarını dene
                    date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d.%m.%Y', '%d-%m-%Y', '%Y/%m/%d']
                    transaction_date = None
                    
                    for fmt in date_formats:
                        try:
                            transaction_date = datetime.strptime(date_str, fmt)
                            print(f"Date parsed successfully with format {fmt}: {transaction_date}")
                            break
                        except ValueError as e:
                            print(f"Date format {fmt} failed: {e}")
                            continue
                    
                    if not transaction_date:
                        print(f"Could not parse date: {date_str}")
                        continue
                        
                except Exception as e:
                    print(f"Date parsing error: {e}")
                    continue
                
                # Tutarı parse et
                try:
                    # Negatif işaret ve para birimi sembollerini temizle
                    amount_str = re.sub(r'[^\d,.-]', '', amount_str)
                    print(f"Amount string after cleaning: {amount_str}")
                    
                    # Boş veya geçersiz tutarları atla
                    if not amount_str or amount_str in ['-', '.', ',']:
                        print(f"Skipping invalid amount: {amount_str}")
                        continue
                    
                    # Türkiye formatı (1.234,56) veya international format (1,234.56)
                    if ',' in amount_str and '.' in amount_str:
                        # Hem virgül hem nokta var, format belirle
                        if amount_str.rfind(',') > amount_str.rfind('.'):
                            # Virgül daha sonda, TR format (1.234,56)
                            amount_str = amount_str.replace('.', '').replace(',', '.')
                        else:
                            # Nokta daha sonda, US format (1,234.56)
                            amount_str = amount_str.replace(',', '')
                    elif ',' in amount_str:
                        # Sadece virgül var
                        parts = amount_str.split(',')
                        if len(parts) == 2 and len(parts[1]) <= 2:
                            # Decimal separator olarak virgül
                            amount_str = amount_str.replace(',', '.')
                        else:
                            # Thousand separator olarak virgül
                            amount_str = amount_str.replace(',', '')
                    
                    # Negatif tutarları pozitif yap (harcama)
                    amount = abs(float(amount_str))
                    print(f"Amount parsed: {amount}")
                    
                    if amount <= 0:
                        print(f"Skipping zero amount transaction")
                        continue
                        
                except Exception as e:
                    print(f"Amount parsing error: {e}")
                    continue
                
                if description and amount > 0:
                    transaction = {
                        'date': transaction_date.strftime('%Y-%m-%d'),
                        'description': description[:100],  # Açıklamayı kısıtla
                        'amount': amount
                    }
                    transactions.append(transaction)
                    print(f"Transaction added: {transaction}")
            
            print(f"Total transactions parsed: {len(transactions)}")
            return transactions
            
        except Exception as e:
            print(f"CSV parse error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_txt_statement(self, file):
        """TXT formatındaki ekstre dosyasını parse et"""
        transactions = []
        try:
            content = file.read().decode('utf-8-sig')
            lines = content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Basit regex pattern'lar ile işlem bilgilerini çıkart
                # Format: "DD/MM/YYYY AÇIKLAMA TUTAR"
                pattern = r'(\d{1,2}[/.]\d{1,2}[/.]\d{2,4})\s+(.+?)\s+(\d+[.,]\d{2})'
                match = re.search(pattern, line)
                
                if match:
                    date_str = match.group(1)
                    description = match.group(2).strip()
                    amount_str = match.group(3)
                    
                    # Tarih parse et
                    try:
                        date_str = date_str.replace('.', '/').replace('-', '/')
                        transaction_date = datetime.strptime(date_str, '%d/%m/%Y')
                    except:
                        try:
                            transaction_date = datetime.strptime(date_str, '%d/%m/%y')
                        except:
                            continue
                    
                    # Tutar parse et
                    try:
                        amount_str = amount_str.replace(',', '.')
                        amount = float(amount_str)
                        if amount > 0:
                            transactions.append({
                                'date': transaction_date.strftime('%Y-%m-%d'),
                                'description': description,
                                'amount': amount
                            })
                    except:
                        continue
            
            return transactions
            
        except Exception as e:
            print(f"TXT parse error: {e}")
            return []
    
    def _analyze_credit_card_statement(self, transactions):
        """Kredi kartı ekstresi AI analizi"""
        try:
            # Temel istatistikler
            total_amount = sum(t['amount'] for t in transactions)
            transaction_count = len(transactions)
            avg_transaction = total_amount / transaction_count if transaction_count > 0 else 0
            
            # Kategori analizi - AI ile her işlemi kategorize et
            analysis_service = ExpenseAnalysisService()
            categorized_transactions = []
            category_totals = {}
            
            for transaction in transactions:
                # Her işlem için AI kategorilendirmesi
                try:
                    ai_analysis = analysis_service.analyze_expense_text(
                        transaction['description'], 
                        transaction['amount']
                    )
                    category = ai_analysis.get('category', 'other')
                    confidence = ai_analysis.get('confidence', 0.5)
                    
                    categorized_transaction = {
                        **transaction,
                        'category': category,
                        'confidence': confidence,
                        'ai_tags': ai_analysis.get('tags', [])
                    }
                    categorized_transactions.append(categorized_transaction)
                    
                    # Kategori toplamları
                    if category not in category_totals:
                        category_totals[category] = {
                            'amount': 0,
                            'count': 0,
                            'transactions': []
                        }
                    
                    category_totals[category]['amount'] += transaction['amount']
                    category_totals[category]['count'] += 1
                    category_totals[category]['transactions'].append(transaction)
                    
                except Exception as e:
                    print(f"Transaction analysis error: {e}")
                    # Fallback kategori
                    categorized_transactions.append({
                        **transaction,
                        'category': 'other',
                        'confidence': 0.3
                    })
            
            # Kategori bilgilerini zenginleştir
            category_mapping = {
                'food': ('🍽️', 'Gıda & İçecek', '#ef4444'),
                'transport': ('🚗', 'Ulaşım', '#3b82f6'),
                'entertainment': ('🎬', 'Eğlence', '#8b5cf6'),
                'bills': ('💡', 'Faturalar', '#f59e0b'),
                'shopping': ('🛍️', 'Alışveriş', '#ec4899'),
                'health': ('🏥', 'Sağlık', '#10b981'),
                'education': ('📚', 'Eğitim', '#06b6d4'),
                'investment': ('📈', 'Yatırım', '#84cc16'),
                'housing': ('🏠', 'Konut', '#f97316'),
                'other': ('📦', 'Diğer', '#6366f1')
            }
            
            category_analysis = {}
            for category, data in category_totals.items():
                icon, name, color = category_mapping.get(category, category_mapping['other'])
                percentage = (data['amount'] / total_amount) * 100 if total_amount > 0 else 0
                
                category_analysis[category] = {
                    'name': name,
                    'icon': icon,
                    'color': color,
                    'amount': data['amount'],
                    'count': data['count'],
                    'percentage': percentage,
                    'avg_amount': data['amount'] / data['count'] if data['count'] > 0 else 0
                }
            
            # En büyük kategoriler
            top_categories = sorted(category_analysis.items(), 
                                  key=lambda x: x[1]['amount'], reverse=True)[:5]
            
            # AI insights üret
            insights = self._generate_spending_insights(category_analysis, categorized_transactions, total_amount)
            
            # Tarih aralığı
            dates = [datetime.strptime(t['date'], '%Y-%m-%d') for t in transactions]
            min_date = min(dates).strftime('%Y-%m-%d') if dates else None
            max_date = max(dates).strftime('%Y-%m-%d') if dates else None
            
            return {
                'summary': {
                    'total_amount': total_amount,
                    'transaction_count': transaction_count,
                    'avg_transaction': avg_transaction,
                    'date_range': {
                        'start': min_date,
                        'end': max_date
                    }
                },
                'category_analysis': category_analysis,
                'top_categories': [
                    {
                        'category': cat[0],
                        'name': cat[1]['name'],
                        'icon': cat[1]['icon'],
                        'amount': cat[1]['amount'],
                        'percentage': cat[1]['percentage']
                    } for cat in top_categories
                ],
                'insights': insights,
                'categorized_transactions': categorized_transactions[:50]  # İlk 50 işlem
            }
            
        except Exception as e:
            print(f"Analysis error: {e}")
            raise
    
    def _generate_spending_insights(self, category_analysis, transactions, total_amount):
        """Harcama analizine dayalı AI insights üret"""
        insights = []
        
        try:
            # En yüksek harcama kategorisi
            if category_analysis:
                top_category = max(category_analysis.items(), key=lambda x: x[1]['amount'])
                top_cat_name = top_category[1]['name']
                top_cat_amount = top_category[1]['amount']
                top_cat_percentage = top_category[1]['percentage']
                
                if top_cat_percentage > 40:
                    insights.append({
                        'type': 'warning',
                        'icon': '⚠️',
                        'title': f'{top_cat_name} Ağırlıklı Harcama',
                        'message': f'Harcamalarınızın %{top_cat_percentage:.1f}\'i {top_cat_name} kategorisinde. Bu dengeyi gözden geçirmek isteyebilirsiniz.',
                        'priority': 4,
                        'amount': top_cat_amount
                    })
                elif top_cat_percentage > 25:
                    insights.append({
                        'type': 'info',
                        'icon': '💡',
                        'title': f'{top_cat_name} Odaklı Bütçe',
                        'message': f'{top_cat_name} harcamalarınız toplam bütçenizin %{top_cat_percentage:.1f}\'ini oluşturuyor.',
                        'priority': 2,
                        'amount': top_cat_amount
                    })
            
            # Ortalama işlem tutarı analizi
            avg_transaction = total_amount / len(transactions) if transactions else 0
            if avg_transaction > 500:
                insights.append({
                    'type': 'suggestion',
                    'icon': '📊',
                    'title': 'Yüksek Ortalama Harcama',
                    'message': f'Ortalama işlem tutarınız ₺{avg_transaction:.2f}. Küçük harcamaları takip etmek tasarrufa yardımcı olabilir.',
                    'priority': 3,
                    'amount': avg_transaction
                })
            
            # Gıda harcamaları özel analizi
            if 'food' in category_analysis:
                food_data = category_analysis['food']
                food_avg = food_data['avg_amount']
                food_count = food_data['count']
                
                if food_avg > 100:
                    insights.append({
                        'type': 'suggestion',
                        'icon': '🍽️',
                        'title': 'Yemek Harcama Optimizasyonu',
                        'message': f'Ortalama yemek harcamanız ₺{food_avg:.2f}. Evde yemek yaparak aylık ₺{(food_avg * food_count * 0.3):.0f} tasarruf edebilirsiniz.',
                        'priority': 3,
                        'amount': food_avg * food_count * 0.3
                    })
            
            # Eğlence harcamaları
            if 'entertainment' in category_analysis:
                ent_data = category_analysis['entertainment']
                if ent_data['percentage'] > 20:
                    insights.append({
                        'type': 'info',
                        'icon': '🎬',
                        'title': 'Eğlence Bütçesi',
                        'message': f'Eğlence harcamalarınız %{ent_data["percentage"]:.1f}. Bu oran dengeyi gösteriyor!',
                        'priority': 1,
                        'amount': ent_data['amount']
                    })
            
            # Genel başarı mesajı
            if len(insights) < 2:
                insights.append({
                    'type': 'achievement',
                    'icon': '🎉',
                    'title': 'Dengeli Harcama Profili',
                    'message': f'{len(transactions)} işleminiz başarıyla analiz edildi. Harcama dağılımınız dengeli görünüyor!',
                    'priority': 1,
                    'amount': total_amount
                })
            
            # Insights'ları önceliğe göre sırala
            insights.sort(key=lambda x: x['priority'], reverse=True)
            
            return insights[:5]  # En fazla 5 insight
            
        except Exception as e:
            print(f"Insights generation error: {e}")
            return [{
                'type': 'info',
                'icon': '📊',
                'title': 'Analiz Tamamlandı',
                'message': f'{len(transactions)} işleminiz başarıyla kategorilere ayrıldı.',
                'priority': 1,
                'amount': total_amount
            }]
    
    def _save_statement_to_db(self, file_name, analysis, transactions):
        """Ekstreyi veritabanına kaydet"""
        try:
            from datetime import datetime
            
            # Ekstre kaydı oluştur
            statement = CreditCardStatement.objects.create(
                # user=request.user,  # Şimdilik user yok
                file_name=file_name,
                total_amount=analysis['summary']['total_amount'],
                transaction_count=analysis['summary']['transaction_count'],
                avg_transaction=analysis['summary']['avg_transaction'],
                start_date=datetime.strptime(analysis['summary']['date_range']['start'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(analysis['summary']['date_range']['end'], '%Y-%m-%d').date(),
                category_analysis=analysis['category_analysis'],
                top_categories=analysis['top_categories'],
                insights=analysis['insights']
            )
            
            # İşlemleri kaydet
            for transaction in analysis['categorized_transactions']:
                StatementTransaction.objects.create(
                    statement=statement,
                    date=datetime.strptime(transaction['date'], '%Y-%m-%d').date(),
                    description=transaction['description'],
                    amount=transaction['amount'],
                    category=transaction['category'],
                    confidence=transaction.get('confidence', 85.0),
                    ai_tags=transaction.get('ai_tags', [])
                )
            
            return statement
            
        except Exception as e:
            print(f"Error saving statement to DB: {e}")
            return None


@method_decorator(csrf_exempt, name='dispatch')
class StatementListView(APIView):
    """Yüklenen ekstreleri listele"""
    permission_classes = [AllowAny]  # Geçici
    
    def get(self, request):
        """Tüm ekstreleri getir"""
        try:
            statements = CreditCardStatement.objects.all().order_by('-upload_date')
            
            statements_data = []
            for statement in statements:
                statements_data.append({
                    'id': statement.id,
                    'file_name': statement.file_name,
                    'upload_date': statement.upload_date.strftime('%Y-%m-%d %H:%M'),
                    'total_amount': float(statement.total_amount),
                    'transaction_count': statement.transaction_count,
                    'avg_transaction': float(statement.avg_transaction),
                    'date_range': {
                        'start': statement.start_date.strftime('%Y-%m-%d'),
                        'end': statement.end_date.strftime('%Y-%m-%d')
                    },
                    'top_category': statement.top_categories[0] if statement.top_categories else None,
                    'insights_count': len(statement.insights) if statement.insights else 0
                })
            
            return Response({
                'statements': statements_data,
                'total_count': len(statements_data)
            })
            
        except Exception as e:
            print(f"Statement list error: {e}")
            return Response({
                'error': 'Ekstreler alınırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StatementDetailView(APIView):
    """Ekstre detayını getir"""
    permission_classes = [AllowAny]  # Geçici
    
    def get(self, request, statement_id):
        """Belirli bir ekstrenin detayını getir"""
        try:
            statement = CreditCardStatement.objects.get(id=statement_id)
            
            # İşlemleri getir
            transactions = []
            for transaction in statement.transactions.all():
                transactions.append({
                    'id': transaction.id,
                    'date': transaction.date.strftime('%Y-%m-%d'),
                    'description': transaction.description,
                    'amount': float(transaction.amount),
                    'category': transaction.category,
                    'confidence': float(transaction.confidence),
                    'ai_tags': transaction.ai_tags
                })
            
            statement_data = {
                'id': statement.id,
                'file_name': statement.file_name,
                'upload_date': statement.upload_date.strftime('%Y-%m-%d %H:%M'),
                'summary': {
                    'total_amount': float(statement.total_amount),
                    'transaction_count': statement.transaction_count,
                    'avg_transaction': float(statement.avg_transaction),
                    'date_range': {
                        'start': statement.start_date.strftime('%Y-%m-%d'),
                        'end': statement.end_date.strftime('%Y-%m-%d')
                    }
                },
                'category_analysis': statement.category_analysis,
                'top_categories': statement.top_categories,
                'insights': statement.insights,
                'categorized_transactions': transactions
            }
            
            return Response(statement_data)
            
        except CreditCardStatement.DoesNotExist:
            return Response({
                'error': 'Ekstre bulunamadı'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Statement detail error: {e}")
            return Response({
                'error': 'Ekstre detayı alınırken hata oluştu'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
