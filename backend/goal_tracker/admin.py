from django.contrib import admin
from .models import FinancialGoal, GoalContribution, GoalMilestone, GoalCategory, GoalReminder


@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'target_amount', 'current_amount', 'progress_percentage', 'target_date', 'priority', 'status']
    list_filter = ['category', 'priority', 'status', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['progress_percentage', 'remaining_amount', 'is_completed', 'months_remaining', 'required_monthly_amount']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('user', 'name', 'description', 'category')
        }),
        ('Finansal Bilgiler', {
            'fields': ('target_amount', 'current_amount', 'monthly_contribution')
        }),
        ('Zaman Bilgileri', {
            'fields': ('target_date', 'created_at', 'updated_at')
        }),
        ('Durum ve Öncelik', {
            'fields': ('priority', 'status', 'is_active')
        }),
        ('Ayarlar', {
            'fields': ('auto_contribute', 'notification_enabled')
        }),
        ('Hesaplanan Değerler', {
            'fields': ('progress_percentage', 'remaining_amount', 'is_completed', 'months_remaining', 'required_monthly_amount'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage', 'remaining_amount', 'is_completed', 'months_remaining', 'required_monthly_amount']


@admin.register(GoalContribution)
class GoalContributionAdmin(admin.ModelAdmin):
    list_display = ['goal', 'amount', 'source', 'date', 'is_recurring']
    list_filter = ['source', 'is_recurring', 'date']
    search_fields = ['goal__name', 'note']
    date_hierarchy = 'date'


@admin.register(GoalMilestone)
class GoalMilestoneAdmin(admin.ModelAdmin):
    list_display = ['goal', 'target_percentage', 'target_amount', 'is_achieved', 'achieved_date']
    list_filter = ['is_achieved', 'target_percentage']
    search_fields = ['goal__name', 'title']


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(GoalReminder)
class GoalReminderAdmin(admin.ModelAdmin):
    list_display = ['goal', 'reminder_type', 'title', 'frequency', 'next_reminder_date', 'is_active']
    list_filter = ['reminder_type', 'frequency', 'is_active']
    search_fields = ['goal__name', 'title']
    date_hierarchy = 'next_reminder_date'
