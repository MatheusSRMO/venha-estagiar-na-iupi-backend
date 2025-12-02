"""
Tests for Use Cases.

This module contains unit tests for the application use cases,
using mock repositories to isolate the business logic.
"""

import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import Mock, MagicMock
from uuid import uuid4

from src.application.dtos import (
    CreateTransactionDTO,
    UpdateTransactionDTO,
    TransactionResponseDTO,
    SummaryResponseDTO,
)
from src.application.use_cases import (
    CreateTransactionUseCase,
    GetTransactionUseCase,
    ListTransactionsUseCase,
    UpdateTransactionUseCase,
    DeleteTransactionUseCase,
    GetSummaryUseCase,
)
from src.domain.entities import Transaction, TransactionType
from src.domain.repositories import TransactionRepositoryInterface


class TestCreateTransactionUseCase:
    """Tests for CreateTransactionUseCase."""

    def test_create_income_transaction(self):
        """Test creating an income transaction."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        
        created_transaction = Transaction(
            id=uuid4(),
            description="Salário",
            amount=Decimal("5000.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 15),
        )
        mock_repo.create.return_value = created_transaction

        use_case = CreateTransactionUseCase(mock_repo)
        dto = CreateTransactionDTO(
            description="Salário",
            amount=Decimal("5000.00"),
            type="income",
            date=date(2025, 1, 15),
        )

        result = use_case.execute(dto)

        assert isinstance(result, TransactionResponseDTO)
        assert result.description == "Salário"
        assert result.type == "income"
        mock_repo.create.assert_called_once()

    def test_create_expense_transaction(self):
        """Test creating an expense transaction."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        
        created_transaction = Transaction(
            id=uuid4(),
            description="Aluguel",
            amount=Decimal("1500.00"),
            type=TransactionType.EXPENSE,
            date=date(2025, 1, 10),
        )
        mock_repo.create.return_value = created_transaction

        use_case = CreateTransactionUseCase(mock_repo)
        dto = CreateTransactionDTO(
            description="Aluguel",
            amount=Decimal("1500.00"),
            type="expense",
            date=date(2025, 1, 10),
        )

        result = use_case.execute(dto)

        assert result.type == "expense"
        assert result.description == "Aluguel"

    def test_create_with_invalid_type_raises_error(self):
        """Test that invalid type raises ValueError."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        use_case = CreateTransactionUseCase(mock_repo)
        
        dto = CreateTransactionDTO(
            description="Test",
            amount=Decimal("100.00"),
            type="invalid",
            date=date(2025, 1, 1),
        )

        with pytest.raises(ValueError, match="Type must be 'income' or 'expense'"):
            use_case.execute(dto)


class TestGetTransactionUseCase:
    """Tests for GetTransactionUseCase."""

    def test_get_existing_transaction(self):
        """Test retrieving an existing transaction."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        transaction_id = uuid4()
        
        transaction = Transaction(
            id=transaction_id,
            description="Salário",
            amount=Decimal("5000.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 15),
        )
        mock_repo.get_by_id.return_value = transaction

        use_case = GetTransactionUseCase(mock_repo)
        result = use_case.execute(transaction_id)

        assert result is not None
        assert result.id == str(transaction_id)
        assert result.description == "Salário"
        mock_repo.get_by_id.assert_called_once_with(transaction_id)

    def test_get_nonexistent_transaction_returns_none(self):
        """Test that getting nonexistent transaction returns None."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.get_by_id.return_value = None

        use_case = GetTransactionUseCase(mock_repo)
        result = use_case.execute(uuid4())

        assert result is None


class TestListTransactionsUseCase:
    """Tests for ListTransactionsUseCase."""

    def test_list_all_transactions(self):
        """Test listing all transactions."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        
        transactions = [
            Transaction(
                id=uuid4(),
                description="Salário",
                amount=Decimal("5000.00"),
                type=TransactionType.INCOME,
                date=date(2025, 1, 15),
            ),
            Transaction(
                id=uuid4(),
                description="Aluguel",
                amount=Decimal("1500.00"),
                type=TransactionType.EXPENSE,
                date=date(2025, 1, 10),
            ),
        ]
        mock_repo.get_all.return_value = (transactions, 2)

        use_case = ListTransactionsUseCase(mock_repo)
        result = use_case.execute()

        assert len(result.data) == 2
        assert result.meta.total_items == 2

    def test_list_with_type_filter(self):
        """Test listing transactions with type filter."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        
        transactions = [
            Transaction(
                id=uuid4(),
                description="Salário",
                amount=Decimal("5000.00"),
                type=TransactionType.INCOME,
                date=date(2025, 1, 15),
            ),
        ]
        mock_repo.get_all.return_value = (transactions, 1)

        use_case = ListTransactionsUseCase(mock_repo)
        result = use_case.execute(transaction_type="income")

        mock_repo.get_all.assert_called_once_with(
            description=None,
            transaction_type="income",
            page=1,
            size=10,
        )

    def test_list_with_description_filter(self):
        """Test listing transactions with description filter."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.get_all.return_value = ([], 0)

        use_case = ListTransactionsUseCase(mock_repo)
        use_case.execute(description="sal")

        mock_repo.get_all.assert_called_once_with(
            description="sal",
            transaction_type=None,
            page=1,
            size=10,
        )

    def test_list_with_pagination(self):
        """Test listing transactions with pagination."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.get_all.return_value = ([], 0)

        use_case = ListTransactionsUseCase(mock_repo)
        use_case.execute(page=2, size=5)

        mock_repo.get_all.assert_called_once_with(
            description=None,
            transaction_type=None,
            page=2,
            size=5,
        )


class TestUpdateTransactionUseCase:
    """Tests for UpdateTransactionUseCase."""

    def test_update_transaction(self):
        """Test updating a transaction."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        transaction_id = uuid4()
        
        existing_transaction = Transaction(
            id=transaction_id,
            description="Salário",
            amount=Decimal("5000.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 15),
        )
        
        updated_transaction = Transaction(
            id=transaction_id,
            description="Salário atualizado",
            amount=Decimal("5500.00"),
            type=TransactionType.INCOME,
            date=date(2025, 1, 15),
        )
        
        mock_repo.get_by_id.return_value = existing_transaction
        mock_repo.update.return_value = updated_transaction

        use_case = UpdateTransactionUseCase(mock_repo)
        dto = UpdateTransactionDTO(
            description="Salário atualizado",
            amount=Decimal("5500.00"),
        )

        result = use_case.execute(transaction_id, dto)

        assert result.description == "Salário atualizado"
        mock_repo.update.assert_called_once()

    def test_update_nonexistent_transaction_returns_none(self):
        """Test that updating nonexistent transaction returns None."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.get_by_id.return_value = None

        use_case = UpdateTransactionUseCase(mock_repo)
        dto = UpdateTransactionDTO(description="Updated")

        result = use_case.execute(uuid4(), dto)

        assert result is None
        mock_repo.update.assert_not_called()


class TestDeleteTransactionUseCase:
    """Tests for DeleteTransactionUseCase."""

    def test_delete_existing_transaction(self):
        """Test deleting an existing transaction."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.delete.return_value = True

        use_case = DeleteTransactionUseCase(mock_repo)
        result = use_case.execute(uuid4())

        assert result is True

    def test_delete_nonexistent_transaction(self):
        """Test deleting a nonexistent transaction."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.delete.return_value = False

        use_case = DeleteTransactionUseCase(mock_repo)
        result = use_case.execute(uuid4())

        assert result is False


class TestGetSummaryUseCase:
    """Tests for GetSummaryUseCase."""

    def test_get_summary(self):
        """Test getting financial summary."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.get_total_income.return_value = Decimal("7000.00")
        mock_repo.get_total_expense.return_value = Decimal("2350.00")

        use_case = GetSummaryUseCase(mock_repo)
        result = use_case.execute()

        assert isinstance(result, SummaryResponseDTO)
        assert result.total_income == "7000.00"
        assert result.total_expense == "2350.00"
        assert result.net_balance == "4650.00"

    def test_get_summary_with_zero_values(self):
        """Test getting summary when no transactions exist."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.get_total_income.return_value = Decimal("0.00")
        mock_repo.get_total_expense.return_value = Decimal("0.00")

        use_case = GetSummaryUseCase(mock_repo)
        result = use_case.execute()

        assert result.total_income == "0.00"
        assert result.total_expense == "0.00"
        assert result.net_balance == "0.00"

    def test_get_summary_with_negative_balance(self):
        """Test getting summary with more expenses than income."""
        mock_repo = Mock(spec=TransactionRepositoryInterface)
        mock_repo.get_total_income.return_value = Decimal("1000.00")
        mock_repo.get_total_expense.return_value = Decimal("1500.00")

        use_case = GetSummaryUseCase(mock_repo)
        result = use_case.execute()

        assert result.net_balance == "-500.00"
