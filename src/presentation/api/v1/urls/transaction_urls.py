"""
Transaction URL routing module.

This module defines the URL patterns for transaction-related endpoints.
"""

from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from src.presentation.api.v1.views import TransactionViewSet, SummaryView


# Create a router that accepts URLs with or without trailing slash
router = DefaultRouter(trailing_slash=False)
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    # Transaction CRUD endpoints via router (without trailing slash)
    path('', include(router.urls)),
    
    # Transaction CRUD endpoints with trailing slash (redirect to same views)
    re_path(r'^transactions/$', TransactionViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^transactions/(?P<pk>[^/.]+)/$', TransactionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    
    # Summary endpoint (both with and without trailing slash)
    path('summary', SummaryView.as_view(), name='summary'),
    path('summary/', SummaryView.as_view(), name='summary-slash'),
]
