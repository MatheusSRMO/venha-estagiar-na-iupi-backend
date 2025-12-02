"""
Transaction repository interface module.

This module defines the abstract interface for transaction data access.
It follows the Repository pattern to decouple domain logic from data persistence.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from src.domain.entities import Transaction


class TransactionRepositoryInterface(ABC):
    """
    Abstract interface for transaction repository.
    
    This interface defines the contract that any transaction repository
    implementation must follow. It allows for easy swapping of data
    persistence mechanisms (e.g., SQLite, PostgreSQL, MongoDB, etc.)
    without changing the business logic.
    """

    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction:
        """
        Creates a new transaction in the data store.
        
        Args:
            transaction: The Transaction entity to persist.
            
        Returns:
            Transaction: The persisted transaction with generated ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        """
        Retrieves a transaction by its unique identifier.
        
        Args:
            transaction_id: The UUID of the transaction to retrieve.
            
        Returns:
            Optional[Transaction]: The transaction if found, None otherwise.
        """
        pass

    @abstractmethod
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
            transaction_type: Optional filter for transaction type ('income' or 'expense').
            page: Page number (1-indexed).
            size: Number of items per page.
            
        Returns:
            tuple[List[Transaction], int]: Tuple of transactions matching the filters and total count.
        """
        pass

    @abstractmethod
    def update(self, transaction: Transaction) -> Transaction:
        """
        Updates an existing transaction in the data store.
        
        Args:
            transaction: The Transaction entity with updated values.
            
        Returns:
            Transaction: The updated transaction.
            
        Raises:
            ValueError: If the transaction does not exist.
        """
        pass

    @abstractmethod
    def delete(self, transaction_id: UUID) -> bool:
        """
        Deletes a transaction from the data store.
        
        Args:
            transaction_id: The UUID of the transaction to delete.
            
        Returns:
            bool: True if deletion was successful, False if transaction not found.
        """
        pass

    @abstractmethod
    def get_total_income(self) -> Decimal:
        """
        Calculates the sum of all income transactions.
        
        Returns:
            Decimal: Total sum of all income transactions.
        """
        pass

    @abstractmethod
    def get_total_expense(self) -> Decimal:
        """
        Calculates the sum of all expense transactions.
        
        Returns:
            Decimal: Total sum of all expense transactions.
        """
        pass
