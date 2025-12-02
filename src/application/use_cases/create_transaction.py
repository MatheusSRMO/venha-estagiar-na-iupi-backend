"""
Create Transaction Use Case module.

This module contains the use case for creating a new transaction.
"""

from src.application.dtos import CreateTransactionDTO, TransactionResponseDTO
from src.domain.entities import Transaction, TransactionType
from src.domain.repositories import TransactionRepositoryInterface


class CreateTransactionUseCase:
    """
    Use case for creating a new transaction.
    
    This use case handles the business logic for creating a transaction,
    including validation and persistence.
    """

    def __init__(self, repository: TransactionRepositoryInterface) -> None:
        """
        Initializes the use case with a repository.
        
        Args:
            repository: The transaction repository implementation.
        """
        self._repository = repository

    def execute(self, dto: CreateTransactionDTO) -> TransactionResponseDTO:
        """
        Executes the create transaction use case.
        
        Args:
            dto: The DTO containing transaction data.
            
        Returns:
            TransactionResponseDTO: The created transaction response.
            
        Raises:
            ValueError: If validation fails.
        """
        # Convert type string to enum
        try:
            transaction_type = TransactionType(dto.type)
        except ValueError:
            raise ValueError("Type must be 'income' or 'expense'.")

        # Create domain entity (validation happens in __post_init__)
        transaction = Transaction(
            description=dto.description,
            amount=dto.amount,
            type=transaction_type,
            date=dto.date,
        )

        # Generate ID and persist
        transaction.generate_id()
        created_transaction = self._repository.create(transaction)

        # Return response DTO
        return TransactionResponseDTO(
            id=str(created_transaction.id),
            description=created_transaction.description,
            amount=str(created_transaction.amount),
            type=created_transaction.type.value,
            date=created_transaction.date.isoformat(),
        )
