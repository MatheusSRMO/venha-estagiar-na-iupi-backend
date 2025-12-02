"""
List Transactions Use Case module.

This module contains the use case for listing transactions with optional filters.
"""

import math
from typing import Optional

from src.application.dtos import (
    TransactionResponseDTO,
    PaginatedTransactionResponseDTO,
    PaginationMetaDTO,
    PaginationLinksDTO,
)
from src.domain.repositories import TransactionRepositoryInterface


class ListTransactionsUseCase:
    """
    Use case for listing transactions with optional filters.
    """

    DEFAULT_PAGE = 1
    DEFAULT_SIZE = 10
    MAX_SIZE = 100

    def __init__(self, repository: TransactionRepositoryInterface) -> None:
        """
        Initializes the use case with a repository.
        
        Args:
            repository: The transaction repository implementation.
        """
        self._repository = repository

    def execute(
        self,
        description: Optional[str] = None,
        transaction_type: Optional[str] = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_SIZE,
        base_url: str = "/transactions",
    ) -> PaginatedTransactionResponseDTO:
        """
        Executes the list transactions use case with pagination.
        
        Args:
            description: Optional filter for description (case-insensitive partial match).
            transaction_type: Optional filter for transaction type ('income' or 'expense').
            page: Page number (1-indexed, defaults to 1).
            size: Number of items per page (defaults to 10, max 100).
            base_url: Base URL for building pagination links.
            
        Returns:
            PaginatedTransactionResponseDTO: Paginated list of transactions.
        """
        page = max(1, page)
        size = max(1, min(size, self.MAX_SIZE))

        transactions, total_count = self._repository.get_all(
            description=description,
            transaction_type=transaction_type,
            page=page,
            size=size,
        )

        total_pages = math.ceil(total_count / size) if total_count > 0 else 1

        data = [
            TransactionResponseDTO(
                id=str(transaction.id),
                description=transaction.description,
                amount=str(transaction.amount),
                type=transaction.type.value,
                date=transaction.date.isoformat(),
            )
            for transaction in transactions
        ]

        meta = PaginationMetaDTO(
            page=page,
            size=size,
            total_pages=total_pages,
            total_items=total_count,
        )

        query_params = self._build_query_params(description, transaction_type)
        links = PaginationLinksDTO(
            self=self._build_link(base_url, page, size, query_params),
            next=self._build_link(base_url, page + 1, size, query_params) if page < total_pages else None,
            prev=self._build_link(base_url, page - 1, size, query_params) if page > 1 else None,
            first=self._build_link(base_url, 1, size, query_params),
            last=self._build_link(base_url, total_pages, size, query_params),
        )

        return PaginatedTransactionResponseDTO(
            data=data,
            meta=meta,
            links=links,
        )

    def _build_query_params(self, description: Optional[str], transaction_type: Optional[str]) -> str:
        """Builds additional query parameters string."""
        params = []
        if description:
            params.append(f"description={description}")
        if transaction_type:
            params.append(f"type={transaction_type}")
        return "&".join(params)

    def _build_link(self, base_url: str, page: int, size: int, query_params: str) -> str:
        """Builds a pagination link."""
        link = f"{base_url}?page={page}&size={size}"
        if query_params:
            link += f"&{query_params}"
        return link
