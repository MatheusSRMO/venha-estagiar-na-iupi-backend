"""
Transaction DTOs (Data Transfer Objects) module.

This module contains DTOs used to transfer data between layers.
DTOs ensure that the domain entities are not exposed directly to the presentation layer.
"""

from dataclasses import dataclass
from datetime import date as Date
from decimal import Decimal
from typing import Optional


@dataclass
class CreateTransactionDTO:
    """
    DTO for creating a new transaction.
    
    Attributes:
        description: Description of the transaction.
        amount: The transaction value (positive number).
        type: The type of transaction ('income' or 'expense').
        date: The date of the transaction.
    """
    description: str
    amount: Decimal
    type: str
    date: Date


@dataclass
class UpdateTransactionDTO:
    """
    DTO for updating an existing transaction.
    
    All fields are optional to support partial updates (PATCH).
    
    Attributes:
        description: Optional new description.
        amount: Optional new amount.
        type: Optional new type.
        date: Optional new date.
    """
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    type: Optional[str] = None
    date: Optional[Date] = None


@dataclass
class TransactionResponseDTO:
    """
    DTO for transaction response.
    
    Attributes:
        id: The transaction's unique identifier.
        description: Description of the transaction.
        amount: The transaction value.
        type: The type of transaction.
        date: The date of the transaction.
    """
    id: str
    description: str
    amount: str
    type: str
    date: str


@dataclass
class SummaryResponseDTO:
    """
    DTO for summary response.
    
    Attributes:
        total_income: Sum of all income transactions.
        total_expense: Sum of all expense transactions.
        net_balance: Difference between income and expense.
    """
    total_income: str
    total_expense: str
    net_balance: str


@dataclass
class PaginationMetaDTO:
    """
    DTO for pagination metadata.
    
    Attributes:
        page: Current page number.
        size: Number of items per page.
        total_pages: Total number of pages.
        total_items: Total number of items.
    """
    page: int
    size: int
    total_pages: int
    total_items: int


@dataclass
class PaginationLinksDTO:
    """
    DTO for pagination links.
    
    Attributes:
        self: Link to the current page.
        next: Link to the next page (None if on last page).
        prev: Link to the previous page (None if on first page).
        first: Link to the first page.
        last: Link to the last page.
    """
    self: str
    next: Optional[str]
    prev: Optional[str]
    first: str
    last: str


@dataclass
class PaginatedTransactionResponseDTO:
    """
    DTO for paginated transaction response.
    
    Attributes:
        data: List of transactions.
        meta: Pagination metadata.
        links: Pagination links.
    """
    data: list
    meta: PaginationMetaDTO
    links: PaginationLinksDTO
