"""
Django admin configuration for Transaction model.
"""

from django.contrib import admin

from src.infrastructure.django_app.models import TransactionModel


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Transaction model.
    """
    list_display = ('id', 'description', 'amount', 'type', 'date', 'created_at')
    list_filter = ('type', 'date')
    search_fields = ('description',)
    ordering = ('-date', '-created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
