from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class AIConversation(models.Model):
    """Kullanıcıların AI ile yaptığı konuşmaları kaydeder"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    session_id = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.session_id}"


class AIMessage(models.Model):
    """Konuşmadaki her mesajı kaydeder"""
    MESSAGE_TYPES = [
        ('text', 'Metin'),
        ('analysis', 'Analiz'),
        ('recommendation', 'Tavsiye'),
    ]
    
    SENDER_TYPES = [
        ('user', 'Kullanıcı'),
        ('bot', 'Bot'),
    ]
    
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_TYPES)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."


class CreditAnalysis(models.Model):
    """Kredi analizi sonuçlarını saklar"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_analyses')
    
    # Finansal veriler
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    existing_debts = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_score = models.IntegerField(null=True, blank=True)
    
    # Analiz sonuçları
    credit_worthiness_score = models.IntegerField()  # 0-100
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    recommended_loan_term = models.IntegerField()  # Ay cinsinden
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
    ])
    
    # Meta
    analysis_date = models.DateTimeField(auto_now_add=True)
    ai_recommendations = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.user.username} - Kredi Analizi ({self.analysis_date.date()})"
