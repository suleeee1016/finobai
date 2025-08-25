from django.urls import path
from .views import (
    ExpenseAnalysisView, 
    MonthlySummaryView, 
    ExpenseCategoriesView,
    CreditCardStatementUploadView,
    StatementListView,
    StatementDetailView
)

urlpatterns = [
    path('analyze/', ExpenseAnalysisView.as_view(), name='expense-analysis'),
    path('summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('categories/', ExpenseCategoriesView.as_view(), name='expense-categories'),
    path('upload-statement/', CreditCardStatementUploadView.as_view(), name='upload-statement'),
    path('statements/', StatementListView.as_view(), name='statement-list'),
    path('statements/<int:statement_id>/', StatementDetailView.as_view(), name='statement-detail'),
]
