from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class ExpenseCategory(models.Model):
    """Harcama kategorileri"""
    
    CATEGORY_CHOICES = [
        ('food', '🍽️ Gıda & İçecek'),
        ('transport', '🚗 Ulaşım'),
        ('entertainment', '🎬 Eğlence'),
        ('bills', '💡 Faturalar'),
        ('shopping', '🛍️ Alışveriş'),
        ('health', '🏥 Sağlık'),
        ('education', '📚 Eğitim'),
        ('investment', '📈 Yatırım'),
        ('housing', '🏠 Konut'),
        ('other', '📦 Diğer')
    ]
    
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    icon = models.CharField(max_length=10, default='📦')
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    budget_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Harcama Kategorisi"
        verbose_name_plural = "Harcama Kategorileri"
    
    def __str__(self):
        return self.get_name_display()


class Expense(models.Model):
    """Kullanıcı harcamaları"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    
    expense_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AI analiz alanları
    is_necessary = models.BooleanField(default=True, help_text="AI tarafından belirlenen gereklilik")
    ai_category_confidence = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    ai_tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = "Harcama"
        verbose_name_plural = "Harcamalar"
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.amount}₺"


class Budget(models.Model):
    """Kullanıcı bütçeleri"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bütçe"
        verbose_name_plural = "Bütçeler"
        unique_together = ['user', 'category', 'month', 'year']
    
    @property
    def remaining_budget(self):
        return self.monthly_limit - self.current_spent
    
    @property
    def budget_percentage_used(self):
        if self.monthly_limit > 0:
            return (self.current_spent / self.monthly_limit) * 100
        return 0
    
    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.month}/{self.year}"


class ExpenseInsight(models.Model):
    """AI tarafından üretilen harcama içgörüleri"""
    
    INSIGHT_TYPES = [
        ('warning', '⚠️ Uyarı'),
        ('suggestion', '💡 Öneri'),
        ('achievement', '🎉 Başarı'),
        ('trend', '📊 Trend')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_insights')
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPES)
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)  # 1-5 (5 en yüksek)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Harcama İçgörüsü"
        verbose_name_plural = "Harcama İçgörüleri"
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_insight_type_display()} - {self.title}"


class CreditCardStatement(models.Model):
    """Yüklenen kredi kartı ekstreleri"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statements', null=True, blank=True)
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    # Analiz sonuçları
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = models.IntegerField()
    avg_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Tarih aralığı
    start_date = models.DateField()
    end_date = models.DateField()
    
    # JSON analiz verileri
    category_analysis = models.JSONField()
    top_categories = models.JSONField()
    insights = models.JSONField()
    
    class Meta:
        verbose_name = "Kredi Kartı Ekstresi"
        verbose_name_plural = "Kredi Kartı Ekstreleri"
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.file_name} - ₺{self.total_amount} ({self.transaction_count} işlem)"


class StatementTransaction(models.Model):
    """Ekstredeki işlemler"""
    
    statement = models.ForeignKey(CreditCardStatement, on_delete=models.CASCADE, related_name='transactions')
    
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, default=85.0)
    ai_tags = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ekstre İşlemi"
        verbose_name_plural = "Ekstre İşlemleri"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.description} - ₺{self.amount}"
