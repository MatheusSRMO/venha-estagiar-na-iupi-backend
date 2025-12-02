"""
URL configuration for Expense Control API project.

This module defines the root URL configuration for the Django project.
All API endpoints are versioned under /api/v1/ for future compatibility.
"""

from django.contrib import admin
from django.urls import path, include

from src.presentation.api.v1.urls import transaction_urlpatterns


urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    
    # API v1 endpoints
    path("api/v1/", include(transaction_urlpatterns)),
]
