"""
Update Transaction Use Case module.

This module contains the use case for updating an existing transaction.
"""

from typing import Optional
from uuid import UUID

from src.application.dtos import UpdateTransactionDTO, TransactionResponseDTO
from src.domain.entities import Transaction, TransactionType
from src.domain.repositories import TransactionRepositoryInterface


class UpdateTransactionUseCase:
    """
    Use case for updating an existing transaction.
    """

    def __init__(self, repository: TransactionRepositoryInterface) -> None:
        """
        Initializes the use case with a repository.
        
        Args:
            repository: The transaction repository implementation.
        """
        self._repository = repository

    def execute(
        self,
        transaction_id: UUID,
        dto: UpdateTransactionDTO,
    ) -> Optional[TransactionResponseDTO]:
        """
        Executes the update transaction use case.
        
        Args:
            transaction_id: The UUID of the transaction to update.
            dto: The DTO containing the fields to update.
            
        Returns:
            Optional[TransactionResponseDTO]: The updated transaction if found, None otherwise.
            
        Raises:
            ValueError: If validation fails.
        """
        # Get existing transaction
        existing_transaction = self._repository.get_by_id(transaction_id)

        if existing_transaction is None:
            return None

        # Prepare updated values
        description = dto.description if dto.description is not None else existing_transaction.description
        amount = dto.amount if dto.amount is not None else existing_transaction.amount
        
        if dto.type is not None:
            try:
                transaction_type = TransactionType(dto.type)
            except ValueError:
                raise ValueError("Type must be 'income' or 'expense'.")
        else:
            transaction_type = existing_transaction.type

        transaction_date = dto.date if dto.date is not None else existing_transaction.date

        # Create updated domain entity (validation happens in __post_init__)
        updated_transaction = Transaction(
            id=transaction_id,
            description=description,
            amount=amount,
            type=transaction_type,
            date=transaction_date,
        )

        # Persist and return
        saved_transaction = self._repository.update(updated_transaction)

        return TransactionResponseDTO(
            id=str(saved_transaction.id),
            description=saved_transaction.description,
            amount=str(saved_transaction.amount),
            type=saved_transaction.type.value,
            date=saved_transaction.date.isoformat(),
        )
