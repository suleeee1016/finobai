from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router yapılandırması
router = DefaultRouter()
router.register(r'goals', views.FinancialGoalViewSet, basename='financialgoal')
router.register(r'contributions', views.GoalContributionViewSet, basename='goalcontribution')

urlpatterns = [
    # Router URL'leri
    path('', include(router.urls)),
    
    # AI Analiz endpoints
    path('analyze/', views.analyze_goal, name='analyze_goal'),
    path('recommendations/', views.user_recommendations, name='user_recommendations'),
    path('personal-analysis/', views.personal_analysis, name='personal_analysis'),
    path('optimize-plan/', views.optimize_savings_plan, name='optimize_savings_plan'),
    
    # Yardımcı endpoints
    path('categories/', views.goal_categories, name='goal_categories'),
]
