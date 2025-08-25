from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models
from .models import FinancialGoal, GoalContribution, GoalMilestone, GoalCategory, GoalReminder
from .serializers import (
    FinancialGoalSerializer, FinancialGoalSummarySerializer,
    GoalContributionSerializer, ContributionCreateSerializer,
    GoalMilestoneSerializer, GoalCategorySerializer,
    GoalReminderSerializer, GoalAnalysisSerializer
)
from .services import GoalAnalysisService, GoalPlanningService


class FinancialGoalViewSet(viewsets.ModelViewSet):
    """Finansal hedefler CRUD işlemleri"""
    serializer_class = FinancialGoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FinancialGoalSummarySerializer
        return FinancialGoalSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_contribution(self, request, pk=None):
        """Hedefe katkı ekle"""
        goal = self.get_object()
        serializer = ContributionCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(goal=goal)
            
            # Hedefin güncel durumunu döndür
            goal_serializer = FinancialGoalSerializer(goal)
            return Response({
                'message': 'Katkı başarıyla eklendi',
                'goal': goal_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def progress_report(self, request, pk=None):
        """Hedef ilerleme raporu"""
        goal = self.get_object()
        
        # Son 30 günlük katkılar
        recent_contributions = GoalContribution.objects.filter(
            goal=goal,
            date__gte=timezone.now() - timezone.timedelta(days=30)
        )
        
        # Milestone durumu
        milestones = goal.milestones.all()
        
        report_data = {
            'goal': FinancialGoalSerializer(goal).data,
            'recent_contributions': GoalContributionSerializer(recent_contributions, many=True).data,
            'milestones': GoalMilestoneSerializer(milestones, many=True).data,
            'statistics': {
                'days_since_creation': (timezone.now().date() - goal.created_at.date()).days,
                'total_contributions': goal.contributions.count(),
                'avg_contribution': float(goal.contributions.aggregate(
                    avg_amount=models.Avg('amount')
                )['avg_amount'] or 0),
                'completion_rate_per_day': float(goal.progress_percentage) / max(
                    (timezone.now().date() - goal.created_at.date()).days, 1
                ),
            }
        }
        
        return Response(report_data)
    
    @action(detail=False, methods=['get'])
    def dashboard_summary(self, request):
        """Dashboard için özet bilgiler"""
        goals = self.get_queryset().filter(is_active=True)
        
        summary = {
            'total_goals': goals.count(),
            'completed_goals': goals.filter(status='completed').count(),
            'active_goals': goals.filter(status='active').count(),
            'total_target_amount': float(sum(goal.target_amount for goal in goals)),
            'total_saved_amount': float(sum(goal.current_amount for goal in goals)),
            'overall_progress': sum(goal.progress_percentage for goal in goals) / goals.count() if goals else 0,
            'monthly_contribution_total': float(sum(goal.monthly_contribution for goal in goals)),
            'goals_by_category': {},
            'upcoming_deadlines': []
        }
        
        # Kategoriye göre dağılım
        for goal in goals:
            category = goal.get_category_display()
            if category not in summary['goals_by_category']:
                summary['goals_by_category'][category] = {
                    'count': 0,
                    'total_target': 0,
                    'total_saved': 0
                }
            summary['goals_by_category'][category]['count'] += 1
            summary['goals_by_category'][category]['total_target'] += float(goal.target_amount)
            summary['goals_by_category'][category]['total_saved'] += float(goal.current_amount)
        
        # Yaklaşan deadline'lar (30 gün içinde)
        upcoming_deadline_date = timezone.now().date() + timezone.timedelta(days=30)
        upcoming_goals = goals.filter(
            target_date__lte=upcoming_deadline_date,
            status='active'
        ).order_by('target_date')
        
        summary['upcoming_deadlines'] = [
            {
                'goal_name': goal.name,
                'target_date': goal.target_date,
                'days_remaining': (goal.target_date - timezone.now().date()).days,
                'progress': float(goal.progress_percentage)
            }
            for goal in upcoming_goals
        ]
        
        return Response(summary)


class GoalContributionViewSet(viewsets.ModelViewSet):
    """Hedef katkıları yönetimi"""
    serializer_class = GoalContributionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GoalContribution.objects.filter(goal__user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContributionCreateSerializer
        return GoalContributionSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_goal(request):
    """Hedef analizi"""
    serializer = GoalAnalysisSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    goal_id = serializer.validated_data['goal_id']
    analysis_type = serializer.validated_data['analysis_type']
    
    # Kullanıcının hedefini doğrula
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)
    
    service = GoalAnalysisService()
    
    if analysis_type == 'progress':
        result = service.analyze_goal_progress(goal_id)
    elif analysis_type == 'recommendation':
        result = service.get_goal_recommendations(request.user.id)
    elif analysis_type == 'timeline':
        timeframe = serializer.validated_data.get('timeframe', '3m')
        result = service.analyze_contribution_patterns(goal_id, timeframe)
    else:
        return Response({'error': 'Desteklenmeyen analiz türü'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_recommendations(request):
    """Kullanıcı için genel öneriler"""
    service = GoalAnalysisService()
    result = service.get_goal_recommendations(request.user.id)
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def personal_analysis(request):
    """Kullanıcının kişisel hedeflerine yönelik detaylı analiz"""
    service = GoalAnalysisService()
    result = service.analyze_personal_goals(request.user.id)
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def optimize_savings_plan(request):
    """Tasarruf planı optimizasyonu"""
    user_goals = FinancialGoal.objects.filter(
        user=request.user,
        is_active=True,
        status='active'
    )
    
    goals_data = []
    for goal in user_goals:
        goals_data.append({
            'id': goal.id,
            'name': goal.name,
            'target_date': goal.target_date,
            'priority': goal.priority,
            'monthly_contribution': float(goal.monthly_contribution),
            'remaining_amount': float(goal.remaining_amount)
        })
    
    service = GoalPlanningService()
    result = service.calculate_optimal_savings_plan(goals_data)
    
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def goal_categories(request):
    """Hedef kategorileri listesi"""
    categories = GoalCategory.objects.filter(is_active=True)
    
    # Varsayılan kategoriler
    default_categories = [
        {'name': 'Ev Almak', 'icon': '🏠', 'color': '#10B981'},
        {'name': 'Araç Almak', 'icon': '🚗', 'color': '#3B82F6'},
        {'name': 'Tatil/Seyahat', 'icon': '🌴', 'color': '#F59E0B'},
        {'name': 'Düğün', 'icon': '💍', 'color': '#EC4899'},
        {'name': 'Eğitim', 'icon': '🎓', 'color': '#8B5CF6'},
        {'name': 'Acil Durum Fonu', 'icon': '🚨', 'color': '#EF4444'},
        {'name': 'Emeklilik', 'icon': '💰', 'color': '#6B7280'},
        {'name': 'Sağlık', 'icon': '🏥', 'color': '#059669'},
        {'name': 'Yatırım', 'icon': '💼', 'color': '#DC2626'},
        {'name': 'Özel Hedef', 'icon': '⭐', 'color': '#7C3AED'},
    ]
    
    serializer = GoalCategorySerializer(categories, many=True)
    
    return Response({
        'custom_categories': serializer.data,
        'default_categories': default_categories
    })
