"""
Django app configuration module.
"""

from django.apps import AppConfig


class DjangoAppConfig(AppConfig):
    """
    Configuration for the Django infrastructure app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.infrastructure.django_app'
    label = 'transactions'
    verbose_name = 'Transactions'
