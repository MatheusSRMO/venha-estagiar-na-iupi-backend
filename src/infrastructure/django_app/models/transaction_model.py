"""
Transaction Django model module.

This module contains the Django ORM model for persisting transactions.
It is specific to the Django framework and should not be used directly
in the domain or application layers.
"""

import uuid

from django.db import models


class TransactionModel(models.Model):
    """
    Django ORM model for Transaction entity.
    
    This model maps the Transaction domain entity to the database.
    It is an implementation detail of the infrastructure layer.
    """

    class TransactionType(models.TextChoices):
        """
        Choices for transaction type field.
        """
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the transaction.",
    )
    description = models.CharField(
        max_length=255,
        help_text="Description of the transaction.",
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="The transaction value (positive number).",
    )
    type = models.CharField(
        max_length=7,
        choices=TransactionType.choices,
        help_text="The type of transaction (income or expense).",
    )
    date = models.DateField(
        help_text="The date of the transaction.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the transaction was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the transaction was last updated.",
    )

    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self) -> str:
        """
        Returns a string representation of the transaction.
        """
        return f"{self.description} - {self.type} - {self.amount}"
