from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek 

from calendar import monthrange

# Create your views here.
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Expense.objects.filter(user=user)

        start = self.request.query_params.get('start_date')
        end = self.request.query_params.get('end_date')
        if start and end:
            qs = qs.filter(date__range=[start, end])
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        expenses = Expense.objects.filter(user=user)
        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])

        total = expenses.aggregate(total=Sum("amount"))["total"] or 0

        category_data = (
            expenses
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )
        category_summary = {item["category"]: float(item["total"]) for item in category_data}

        daily_data = (
            expenses
            .annotate(day=TruncDay("date"))
            .values("day")
            .annotate(total=Sum("amount"))
            .order_by("day")
        )
        daily_summary = {str(item["day"]): {
            "total": float(item["total"]),
            "average": float(item["total"])
            }
            for item in daily_data
        }

        monthly_data = (
            expenses
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )
        monthly_summary = {
            str(item["month"]): {
            "total": float(item["total"]),
            "average": round(
            float(item["total"]) / monthrange(item["month"].year, item["month"].month)[1], 2
            )}
            for item in monthly_data
        }
        
        weekly_data = (
            expenses
            .annotate(week=TruncWeek("date"))
            .values("week")
            .annotate(total=Sum("amount"))
            .order_by("week")
        )
        weekly_summary = {
            str(item["week"]): {
            "total": float(item["total"]),
            "average": round(float(item["total"]) / 7, 2)
            }
            for item in weekly_data
        }


        return Response({
            "total_expenses": float(total),
            "category_breakdown": category_summary,
            "daily_trends": daily_summary,
            "weekly_trends": weekly_summary,
            "monthly_trends": monthly_summary,
        })