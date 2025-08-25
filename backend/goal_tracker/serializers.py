from rest_framework import serializers
from django.utils import timezone
from decimal import Decimal
from .models import FinancialGoal, GoalContribution, GoalMilestone, GoalCategory, GoalReminder
from django.contrib.auth.models import User


class GoalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalCategory
        fields = '__all__'


class GoalMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalMilestone
        fields = '__all__'
        read_only_fields = ['achieved_date']


class GoalContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalContribution
        fields = '__all__'
        read_only_fields = ['date']


class GoalReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalReminder
        fields = '__all__'
        read_only_fields = ['created_at']


class FinancialGoalSerializer(serializers.ModelSerializer):
    # İlişkili veriler
    contributions = GoalContributionSerializer(many=True, read_only=True)
    milestones = GoalMilestoneSerializer(many=True, read_only=True)
    reminders = GoalReminderSerializer(many=True, read_only=True)
    
    # Hesaplanan alanlar
    progress_percentage = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    months_remaining = serializers.ReadOnlyField()
    required_monthly_amount = serializers.ReadOnlyField()
    
    # Kullanıcı bilgisi
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = FinancialGoal
        fields = [
            'id', 'user', 'user_name', 'name', 'description', 'category',
            'target_amount', 'current_amount', 'target_date', 
            'monthly_contribution', 'priority', 'status', 'is_active',
            'auto_contribute', 'notification_enabled',
            'created_at', 'updated_at',
            'progress_percentage', 'remaining_amount', 'is_completed',
            'months_remaining', 'required_monthly_amount',
            'contributions', 'milestones', 'reminders'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Hedef oluştururken otomatik milestone'ları da oluştur"""
        validated_data['user'] = self.context['request'].user
        goal = super().create(validated_data)
        
        # Otomatik milestone'ları oluştur
        milestones_data = [
            {'title': 'İlk Adım', 'target_percentage': 25},
            {'title': 'Yarı Yol', 'target_percentage': 50},
            {'title': 'Üçte İki', 'target_percentage': 75},
            {'title': 'Hedef Tamamlandı', 'target_percentage': 100},
        ]
        
        for milestone_data in milestones_data:
            GoalMilestone.objects.create(
                goal=goal,
                title=milestone_data['title'],
                target_percentage=milestone_data['target_percentage'],
                target_amount=goal.target_amount * (Decimal(str(milestone_data['target_percentage'])) / Decimal('100')),
            )
        
        return goal


class FinancialGoalSummarySerializer(serializers.ModelSerializer):
    """Liste görünümü için daha basit serializer"""
    progress_percentage = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    months_remaining = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = FinancialGoal
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'target_amount', 'current_amount', 'target_date',
            'priority', 'priority_display', 'status', 'status_display',
            'progress_percentage', 'remaining_amount', 'is_completed',
            'months_remaining', 'created_at'
        ]


class ContributionCreateSerializer(serializers.ModelSerializer):
    """Katkı ekleme için serializer"""
    class Meta:
        model = GoalContribution
        fields = ['goal', 'amount', 'source', 'note', 'is_recurring', 'next_contribution_date']
    
    def create(self, validated_data):
        """Katkı oluştururken hedefin mevcut tutarını güncelle"""
        contribution = super().create(validated_data)
        goal = contribution.goal
        goal.current_amount += contribution.amount
        goal.save()
        
        # Milestone kontrolü yap
        self._check_milestones(goal)
        
        return contribution
    
    def _check_milestones(self, goal):
        """Milestone'ları kontrol et ve gerekirse güncelle"""
        current_percentage = goal.progress_percentage
        
        milestones = goal.milestones.filter(
            is_achieved=False,
            target_percentage__lte=current_percentage
        )
        
        for milestone in milestones:
            milestone.is_achieved = True
            milestone.achieved_date = timezone.now()
            milestone.save()


class GoalAnalysisSerializer(serializers.Serializer):
    """AI analizi için serializer"""
    goal_id = serializers.IntegerField()
    analysis_type = serializers.ChoiceField(choices=[
        ('progress', 'İlerleme Analizi'),
        ('recommendation', 'Öneri Analizi'),
        ('timeline', 'Zaman Çizelgesi Analizi'),
        ('budget', 'Bütçe Analizi')
    ])
    timeframe = serializers.ChoiceField(
        choices=[('1m', '1 Ay'), ('3m', '3 Ay'), ('6m', '6 Ay'), ('1y', '1 Yıl')],
        default='3m'
    )
