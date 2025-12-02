"""
Get Summary Use Case module.

This module contains the use case for getting the financial summary.
"""

from src.application.dtos import SummaryResponseDTO
from src.domain.repositories import TransactionRepositoryInterface


class GetSummaryUseCase:
    """
    Use case for getting the financial summary.
    
    This use case calculates the total income, total expense,
    and net balance from all transactions.
    """

    def __init__(self, repository: TransactionRepositoryInterface) -> None:
        """
        Initializes the use case with a repository.
        
        Args:
            repository: The transaction repository implementation.
        """
        self._repository = repository

    def execute(self) -> SummaryResponseDTO:
        """
        Executes the get summary use case.
        
        Returns:
            SummaryResponseDTO: The financial summary.
        """
        total_income = self._repository.get_total_income()
        total_expense = self._repository.get_total_expense()
        net_balance = total_income - total_expense

        return SummaryResponseDTO(
            total_income=f"{total_income:.2f}",
            total_expense=f"{total_expense:.2f}",
            net_balance=f"{net_balance:.2f}",
        )
