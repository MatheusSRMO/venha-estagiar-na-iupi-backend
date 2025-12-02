"""
Tests for the Transaction entity.

This module contains unit tests for the Transaction domain entity,
testing validation rules and business logic.
"""

import pytest
from datetime import date
from decimal import Decimal
from uuid import UUID

from src.domain.entities import Transaction, TransactionType


class TestTransactionEntity:
    """Tests for Transaction entity creation and validation."""

    def test_create_valid_income_transaction(self):
        """Test creating a valid income transaction."""
        transaction = Transaction(
            description="Salário",
            amount=Decimal("5000.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 15),
        )

        assert transaction.description == "Salário"
        assert transaction.amount == Decimal("5000.00")
        assert transaction.type == TransactionType.INCOME
        assert transaction.date == date(2025, 1, 15)
        assert transaction.id is None

    def test_create_valid_expense_transaction(self):
        """Test creating a valid expense transaction."""
        transaction = Transaction(
            description="Aluguel",
            amount=Decimal("1500.00"),
            type=TransactionType.EXPENSE,
            date=date(2025, 1, 10),
        )

        assert transaction.description == "Aluguel"
        assert transaction.amount == Decimal("1500.00")
        assert transaction.type == TransactionType.EXPENSE
        assert transaction.date == date(2025, 1, 10)

    def test_generate_id(self):
        """Test that generate_id creates a valid UUID."""
        transaction = Transaction(
            description="Test",
            amount=Decimal("100.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 1),
        )

        assert transaction.id is None
        transaction.generate_id()
        assert transaction.id is not None
        assert isinstance(transaction.id, UUID)

    def test_generate_id_does_not_override_existing_id(self):
        """Test that generate_id does not override an existing ID."""
        from uuid import uuid4
        
        existing_id = uuid4()
        transaction = Transaction(
            id=existing_id,
            description="Test",
            amount=Decimal("100.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 1),
        )

        transaction.generate_id()
        assert transaction.id == existing_id

    def test_to_dict(self):
        """Test converting transaction to dictionary."""
        from uuid import uuid4
        
        transaction_id = uuid4()
        transaction = Transaction(
            id=transaction_id,
            description="Salário",
            amount=Decimal("5000.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 15),
        )

        result = transaction.to_dict()

        assert result["id"] == str(transaction_id)
        assert result["description"] == "Salário"
        assert result["amount"] == "5000.00"
        assert result["type"] == "income"
        assert result["date"] == "2025-01-15"


class TestTransactionValidation:
    """Tests for Transaction entity validation rules."""

    def test_empty_description_raises_error(self):
        """Test that empty description raises ValueError."""
        with pytest.raises(ValueError, match="Description is required"):
            Transaction(
                description="",
                amount=Decimal("100.00"),
                type=TransactionType.INCOME,
                date=date(2025, 1, 1),
            )

    def test_whitespace_description_raises_error(self):
        """Test that whitespace-only description raises ValueError."""
        with pytest.raises(ValueError, match="Description is required"):
            Transaction(
                description="   ",
                amount=Decimal("100.00"),
                type=TransactionType.INCOME,
                date=date(2025, 1, 1),
            )

    def test_zero_amount_raises_error(self):
        """Test that zero amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            Transaction(
                description="Test",
                amount=Decimal("0.00"),
                type=TransactionType.INCOME,
                date=date(2025, 1, 1),
            )

    def test_negative_amount_raises_error(self):
        """Test that negative amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            Transaction(
                description="Test",
                amount=Decimal("-100.00"),
                type=TransactionType.INCOME,
                date=date(2025, 1, 1),
            )

    def test_none_amount_raises_error(self):
        """Test that None amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount is required"):
            Transaction(
                description="Test",
                amount=None,
                type=TransactionType.INCOME,
                date=date(2025, 1, 1),
            )

    def test_none_date_raises_error(self):
        """Test that None date raises ValueError."""
        with pytest.raises(ValueError, match="Date is required"):
            Transaction(
                description="Test",
                amount=Decimal("100.00"),
                type=TransactionType.INCOME,
                date=None,
            )


class TestTransactionType:
    """Tests for TransactionType enum."""

    def test_income_value(self):
        """Test that INCOME has correct value."""
        assert TransactionType.INCOME.value == "income"

    def test_expense_value(self):
        """Test that EXPENSE has correct value."""
        assert TransactionType.EXPENSE.value == "expense"

    def test_create_from_string_income(self):
        """Test creating TransactionType from 'income' string."""
        transaction_type = TransactionType("income")
        assert transaction_type == TransactionType.INCOME

    def test_create_from_string_expense(self):
        """Test creating TransactionType from 'expense' string."""
        transaction_type = TransactionType("expense")
        assert transaction_type == TransactionType.EXPENSE

    def test_invalid_type_raises_error(self):
        """Test that invalid type string raises ValueError."""
        with pytest.raises(ValueError):
            TransactionType("invalid")
