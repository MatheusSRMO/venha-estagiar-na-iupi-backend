"""
Pytest configuration and fixtures for the test suite.

This module provides shared fixtures used across all test modules.
"""

import pytest
from datetime import date
from decimal import Decimal
from uuid import uuid4

from rest_framework.test import APIClient

from src.domain.entities import Transaction, TransactionType
from src.infrastructure.django_app.models import TransactionModel


@pytest.fixture
def api_client():
    """
    Provides a DRF APIClient instance for making HTTP requests.
    
    Returns:
        APIClient: Configured API client for testing.
    """
    return APIClient()


@pytest.fixture
def sample_transaction_data():
    """
    Provides sample transaction data for creating transactions.
    
    Returns:
        dict: Valid transaction data.
    """
    return {
        "description": "Salário",
        "amount": "5000.00",
        "type": "income",
        "date": "2025-01-15",
    }


@pytest.fixture
def sample_expense_data():
    """
    Provides sample expense transaction data.
    
    Returns:
        dict: Valid expense transaction data.
    """
    return {
        "description": "Aluguel",
        "amount": "1500.00",
        "type": "expense",
        "date": "2025-01-10",
    }


@pytest.fixture
def sample_transaction_entity():
    """
    Provides a sample Transaction domain entity.
    
    Returns:
        Transaction: Valid transaction entity.
    """
    return Transaction(
        id=uuid4(),
        description="Salário",
        amount=Decimal("5000.00"),
        type=TransactionType.INCOME,
        date=date(2025, 1, 15),
    )


@pytest.fixture
def sample_expense_entity():
    """
    Provides a sample expense Transaction domain entity.
    
    Returns:
        Transaction: Valid expense transaction entity.
    """
    return Transaction(
        id=uuid4(),
        description="Aluguel",
        amount=Decimal("1500.00"),
        type=TransactionType.EXPENSE,
        date=date(2025, 1, 10),
    )


@pytest.fixture
def created_transaction(db, sample_transaction_data):
    """
    Creates a transaction in the database and returns it.
    
    Args:
        db: Database access fixture.
        sample_transaction_data: Sample transaction data.
        
    Returns:
        TransactionModel: Created transaction model instance.
    """
    return TransactionModel.objects.create(
        description=sample_transaction_data["description"],
        amount=Decimal(sample_transaction_data["amount"]),
        type=sample_transaction_data["type"],
        date=date.fromisoformat(sample_transaction_data["date"]),
    )


@pytest.fixture
def created_expense(db, sample_expense_data):
    """
    Creates an expense transaction in the database.
    
    Args:
        db: Database access fixture.
        sample_expense_data: Sample expense data.
        
    Returns:
        TransactionModel: Created expense transaction model instance.
    """
    return TransactionModel.objects.create(
        description=sample_expense_data["description"],
        amount=Decimal(sample_expense_data["amount"]),
        type=sample_expense_data["type"],
        date=date.fromisoformat(sample_expense_data["date"]),
    )


@pytest.fixture
def multiple_transactions(db):
    """
    Creates multiple transactions for testing listing and filtering.
    
    Args:
        db: Database access fixture.
        
    Returns:
        list[TransactionModel]: List of created transactions.
    """
    transactions = [
        TransactionModel.objects.create(
            description="Salário",
            amount=Decimal("5000.00"),
            type="income",
            date=date(2025, 1, 15),
        ),
        TransactionModel.objects.create(
            description="Freelance",
            amount=Decimal("2000.00"),
            type="income",
            date=date(2025, 1, 20),
        ),
        TransactionModel.objects.create(
            description="Aluguel",
            amount=Decimal("1500.00"),
            type="expense",
            date=date(2025, 1, 10),
        ),
        TransactionModel.objects.create(
            description="Café",
            amount=Decimal("50.00"),
            type="expense",
            date=date(2025, 1, 12),
        ),
        TransactionModel.objects.create(
            description="Supermercado",
            amount=Decimal("800.00"),
            type="expense",
            date=date(2025, 1, 14),
        ),
    ]
    return transactions
