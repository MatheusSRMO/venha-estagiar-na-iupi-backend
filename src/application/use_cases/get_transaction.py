"""
Get Transaction Use Case module.

This module contains the use case for retrieving a single transaction by ID.
"""

from typing import Optional
from uuid import UUID

from src.application.dtos import TransactionResponseDTO
from src.domain.repositories import TransactionRepositoryInterface


class GetTransactionUseCase:
    """
    Use case for retrieving a transaction by its ID.
    """

    def __init__(self, repository: TransactionRepositoryInterface) -> None:
        """
        Initializes the use case with a repository.
        
        Args:
            repository: The transaction repository implementation.
        """
        self._repository = repository

    def execute(self, transaction_id: UUID) -> Optional[TransactionResponseDTO]:
        """
        Executes the get transaction use case.
        
        Args:
            transaction_id: The UUID of the transaction to retrieve.
            
        Returns:
            Optional[TransactionResponseDTO]: The transaction if found, None otherwise.
        """
        transaction = self._repository.get_by_id(transaction_id)

        if transaction is None:
            return None

        return TransactionResponseDTO(
            id=str(transaction.id),
            description=transaction.description,
            amount=str(transaction.amount),
            type=transaction.type.value,
            date=transaction.date.isoformat(),
        )
