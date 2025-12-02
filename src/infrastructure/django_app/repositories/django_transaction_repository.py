"""
Django Transaction Repository module.

This module contains the Django-specific implementation of the
TransactionRepositoryInterface. It uses Django ORM for data persistence.
"""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from django.db.models import Sum

from src.domain.entities import Transaction, TransactionType
from src.domain.repositories import TransactionRepositoryInterface
from src.infrastructure.django_app.models import TransactionModel


class DjangoTransactionRepository(TransactionRepositoryInterface):
    """
    Django ORM implementation of the TransactionRepositoryInterface.
    
    This class implements the repository interface using Django's ORM,
    providing concrete data access methods for transactions.
    """

    def _to_domain(self, model: TransactionModel) -> Transaction:
        """
        Converts a Django model instance to a domain entity.
        
        Args:
            model: The Django model instance.
            
        Returns:
            Transaction: The corresponding domain entity.
        """
        return Transaction(
            id=model.id,
            description=model.description,
            amount=model.amount,
            type=TransactionType(model.type),
            date=model.date,
        )

    def _to_model_data(self, transaction: Transaction) -> dict:
        """
        Converts a domain entity to model data dictionary.
        
        Args:
            transaction: The domain entity.
            
        Returns:
            dict: Dictionary with model field values.
        """
        return {
            'id': transaction.id,
            'description': transaction.description,
            'amount': transaction.amount,
            'type': transaction.type.value,
            'date': transaction.date,
        }

    def create(self, transaction: Transaction) -> Transaction:
        """
        Creates a new transaction in the database.
        
        Args:
            transaction: The Transaction entity to persist.
            
        Returns:
            Transaction: The persisted transaction.
        """
        model_data = self._to_model_data(transaction)
        model = TransactionModel.objects.create(**model_data)
        return self._to_domain(model)

    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        """
        Retrieves a transaction by its unique identifier.
        
        Args:
            transaction_id: The UUID of the transaction to retrieve.
            
        Returns:
            Optional[Transaction]: The transaction if found, None otherwise.
        """
        try:
            model = TransactionModel.objects.get(id=transaction_id)
            return self._to_domain(model)
        except TransactionModel.DoesNotExist:
            return None

    def get_all(
        self,
        description: Optional[str] = None,
        transaction_type: Optional[str] = None,
        page: int = 1,
        size: int = 10,
    ) -> tuple[List[Transaction], int]:
        """
        Retrieves all transactions, optionally filtered, with pagination.
        
        Args:
            description: Optional filter for description (case-insensitive partial match).
            transaction_type: Optional filter for transaction type.
            page: Page number (1-indexed).
            size: Number of items per page.
            
        Returns:
            tuple[List[Transaction], int]: Tuple of transactions matching the filters and total count.
        """
        queryset = TransactionModel.objects.all()

        if description:
            queryset = queryset.filter(description__icontains=description)

        if transaction_type:
            queryset = queryset.filter(type=transaction_type)

        total_count = queryset.count()
        
        offset = (page - 1) * size
        queryset = queryset[offset:offset + size]

        return [self._to_domain(model) for model in queryset], total_count

    def update(self, transaction: Transaction) -> Transaction:
        """
        Updates an existing transaction in the database.
        
        Args:
            transaction: The Transaction entity with updated values.
            
        Returns:
            Transaction: The updated transaction.
            
        Raises:
            ValueError: If the transaction does not exist.
        """
        try:
            model = TransactionModel.objects.get(id=transaction.id)
        except TransactionModel.DoesNotExist:
            raise ValueError(f"Transaction with id {transaction.id} not found.")

        model.description = transaction.description
        model.amount = transaction.amount
        model.type = transaction.type.value
        model.date = transaction.date
        model.save()

        return self._to_domain(model)

    def delete(self, transaction_id: UUID) -> bool:
        """
        Deletes a transaction from the database.
        
        Args:
            transaction_id: The UUID of the transaction to delete.
            
        Returns:
            bool: True if deletion was successful, False if transaction not found.
        """
        try:
            model = TransactionModel.objects.get(id=transaction_id)
            model.delete()
            return True
        except TransactionModel.DoesNotExist:
            return False

    def get_total_income(self) -> Decimal:
        """
        Calculates the sum of all income transactions.
        
        Returns:
            Decimal: Total sum of all income transactions.
        """
        result = TransactionModel.objects.filter(
            type=TransactionModel.TransactionType.INCOME
        ).aggregate(total=Sum('amount'))
        
        return result['total'] or Decimal('0.00')

    def get_total_expense(self) -> Decimal:
        """
        Calculates the sum of all expense transactions.
        
        Returns:
            Decimal: Total sum of all expense transactions.
        """
        result = TransactionModel.objects.filter(
            type=TransactionModel.TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))
        
        return result['total'] or Decimal('0.00')
