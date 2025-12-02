"""
Delete Transaction Use Case module.

This module contains the use case for deleting a transaction.
"""

from uuid import UUID

from src.domain.repositories import TransactionRepositoryInterface


class DeleteTransactionUseCase:
    """
    Use case for deleting a transaction.
    """

    def __init__(self, repository: TransactionRepositoryInterface) -> None:
        """
        Initializes the use case with a repository.
        
        Args:
            repository: The transaction repository implementation.
        """
        self._repository = repository

    def execute(self, transaction_id: UUID) -> bool:
        """
        Executes the delete transaction use case.
        
        Args:
            transaction_id: The UUID of the transaction to delete.
            
        Returns:
            bool: True if deletion was successful, False if transaction not found.
        """
        return self._repository.delete(transaction_id)
