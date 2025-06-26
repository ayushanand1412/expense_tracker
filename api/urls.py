from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, ExpenseAnalyticsView

router = DefaultRouter()
router.register('expenses', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('expenses/analytics/', ExpenseAnalyticsView.as_view(), name='expense-analytics'),
    path('', include(router.urls)),
]