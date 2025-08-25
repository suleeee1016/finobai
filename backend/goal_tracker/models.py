from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class FinancialGoal(models.Model):
    """Finansal hedefler modeli"""
    
    CATEGORY_CHOICES = [
        ('house', '🏠 Ev Almak'),
        ('car', '🚗 Araç Almak'),
        ('vacation', '🌴 Tatil/Seyahat'),
        ('wedding', '💍 Düğün'),
        ('education', '🎓 Eğitim'),
        ('emergency', '🚨 Acil Durum Fonu'),
        ('retirement', '💰 Emeklilik'),
        ('health', '🏥 Sağlık'),
        ('investment', '💼 Yatırım'),
        ('custom', '⭐ Özel Hedef')
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Yüksek'),
        (2, 'Orta'), 
        (3, 'Düşük')
    ]
    
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('completed', 'Tamamlandı'),
        ('paused', 'Durduruldu'),
        ('cancelled', 'İptal Edildi')
    ]
    
    # Temel bilgiler
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_goals')
    name = models.CharField(max_length=200, verbose_name='Hedef Adı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Kategori')
    
    # Finansal bilgiler
    target_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name='Hedef Tutar'
    )
    current_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Mevcut Tutar'
    )
    
    # Zaman bilgileri
    target_date = models.DateField(verbose_name='Hedef Tarihi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Planlama bilgileri
    monthly_contribution = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Aylık Katkı'
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, 
        default=2,
        verbose_name='Öncelik'
    )
    
    # Durum bilgileri
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name='Durum'
    )
    is_active = models.BooleanField(default=True)
    
    # AI ve analiz için
    auto_contribute = models.BooleanField(default=False, verbose_name='Otomatik Katkı')
    notification_enabled = models.BooleanField(default=True, verbose_name='Bildirimler')
    
    class Meta:
        verbose_name = 'Finansal Hedef'
        verbose_name_plural = 'Finansal Hedefler'
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return f"{self.name} - ₺{self.target_amount}"
    
    @property
    def progress_percentage(self):
        """Hedefin tamamlanma yüzdesi"""
        if self.target_amount == 0:
            return 0
        return min((self.current_amount / self.target_amount) * 100, 100)
    
    @property
    def remaining_amount(self):
        """Hedefe kalan tutar"""
        return max(self.target_amount - self.current_amount, 0)
    
    @property
    def is_completed(self):
        """Hedef tamamlandı mı?"""
        return self.current_amount >= self.target_amount
    
    @property
    def months_remaining(self):
        """Hedefe kalan ay sayısı"""
        from datetime import date
        if self.target_date <= date.today():
            return 0
        
        today = date.today()
        months = (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month)
        return max(months, 0)
    
    @property
    def required_monthly_amount(self):
        """Hedefe ulaşmak için gereken aylık tutar"""
        remaining = self.remaining_amount
        months = self.months_remaining
        
        if months <= 0:
            return remaining
        return remaining / months


class GoalContribution(models.Model):
    """Hedef katkıları modeli"""
    
    SOURCE_CHOICES = [
        ('manual', 'Manuel'),
        ('automatic', 'Otomatik'),
        ('bonus', 'İkramiye/Bonus'),
        ('salary', 'Maaş Kesintisi'),
        ('transfer', 'Transfer')
    ]
    
    goal = models.ForeignKey(
        FinancialGoal, 
        on_delete=models.CASCADE, 
        related_name='contributions'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Katkı Tutarı'
    )
    source = models.CharField(
        max_length=20, 
        choices=SOURCE_CHOICES, 
        default='manual',
        verbose_name='Kaynak'
    )
    note = models.TextField(blank=True, verbose_name='Not')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')
    
    # Otomatik katkı bilgileri
    is_recurring = models.BooleanField(default=False, verbose_name='Tekrarlanan')
    next_contribution_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Hedef Katkısı'
        verbose_name_plural = 'Hedef Katkıları'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.goal.name} - ₺{self.amount}"


class GoalMilestone(models.Model):
    """Hedef kilometre taşları (25%, 50%, 75%, 100%)"""
    
    goal = models.ForeignKey(
        FinancialGoal, 
        on_delete=models.CASCADE, 
        related_name='milestones'
    )
    title = models.CharField(max_length=100, verbose_name='Başlık')
    target_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Hedef Yüzdesi'
    )
    target_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name='Hedef Tutar'
    )
    achieved_date = models.DateTimeField(null=True, blank=True, verbose_name='Başarıldığı Tarih')
    is_achieved = models.BooleanField(default=False, verbose_name='Başarıldı')
    
    # Ödül ve motivasyon
    reward_text = models.CharField(max_length=200, blank=True, verbose_name='Ödül Metni')
    celebration_message = models.TextField(blank=True, verbose_name='Kutlama Mesajı')
    
    class Meta:
        verbose_name = 'Hedef Kilometre Taşı'
        verbose_name_plural = 'Hedef Kilometre Taşları'
        ordering = ['target_percentage']
        unique_together = ['goal', 'target_percentage']
    
    def __str__(self):
        return f"{self.goal.name} - %{self.target_percentage}"


class GoalCategory(models.Model):
    """Özel hedef kategorileri"""
    
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=10, default='⭐')
    color = models.CharField(max_length=7, default='#10B981')  # Hex color
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Hedef Kategorisi'
        verbose_name_plural = 'Hedef Kategorileri'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class GoalReminder(models.Model):
    """Hedef hatırlatmaları"""
    
    REMINDER_TYPE_CHOICES = [
        ('contribution', 'Katkı Hatırlatması'),
        ('deadline', 'Deadline Hatırlatması'),
        ('milestone', 'Milestone Hatırlatması'),
        ('review', 'Gözden Geçirme')
    ]
    
    FREQUENCY_CHOICES = [
        ('daily', 'Günlük'),
        ('weekly', 'Haftalık'),
        ('monthly', 'Aylık'),
        ('once', 'Tek Seferlik')
    ]
    
    goal = models.ForeignKey(
        FinancialGoal, 
        on_delete=models.CASCADE, 
        related_name='reminders'
    )
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly')
    next_reminder_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Hedef Hatırlatması'
        verbose_name_plural = 'Hedef Hatırlatmaları'
        ordering = ['next_reminder_date']
    
    def __str__(self):
        return f"{self.goal.name} - {self.title}"
