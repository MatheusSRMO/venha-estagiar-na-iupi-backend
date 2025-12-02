"""
Transaction entity module.

This module contains the Transaction domain entity which represents
a financial transaction in the expense control system.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class TransactionType(Enum):
    """
    Enum representing the type of a financial transaction.
    
    Attributes:
        INCOME: Represents money coming in (entrada).
        EXPENSE: Represents money going out (saída).
    """
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    """
    Domain entity representing a financial transaction.
    
    This is a pure domain object with no dependencies on external frameworks.
    It contains the core business logic and validation rules for transactions.
    
    Attributes:
        id: Unique identifier for the transaction.
        description: Description of the transaction (e.g., "Salário", "Aluguel").
        amount: The transaction value. Must be a positive number.
        type: The type of transaction (income or expense).
        date: The date when the transaction occurred.
    """
    description: str
    amount: Decimal
    type: TransactionType
    date: date
    id: Optional[UUID] = None

    def __post_init__(self) -> None:
        """
        Validates the transaction after initialization.
        
        Raises:
            ValueError: If validation fails.
        """
        self._validate()

    def _validate(self) -> None:
        """
        Validates all transaction fields.
        
        Raises:
            ValueError: If any field is invalid.
        """
        self._validate_description()
        self._validate_amount()
        self._validate_type()
        self._validate_date()

    def _validate_description(self) -> None:
        """
        Validates the description field.
        
        Raises:
            ValueError: If description is empty or only whitespace.
        """
        if not self.description or not self.description.strip():
            raise ValueError("Description is required and cannot be empty.")

    def _validate_amount(self) -> None:
        """
        Validates the amount field.
        
        Raises:
            ValueError: If amount is not a positive number.
        """
        if self.amount is None:
            raise ValueError("Amount is required.")
        if not isinstance(self.amount, Decimal):
            raise ValueError("Amount must be a Decimal.")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")

    def _validate_type(self) -> None:
        """
        Validates the type field.
        
        Raises:
            ValueError: If type is not a valid TransactionType.
        """
        if not isinstance(self.type, TransactionType):
            raise ValueError("Type must be 'income' or 'expense'.")

    def _validate_date(self) -> None:
        """
        Validates the date field.
        
        Raises:
            ValueError: If date is not provided.
        """
        if self.date is None:
            raise ValueError("Date is required.")

    def generate_id(self) -> None:
        """
        Generates a new UUID for the transaction if not already set.
        """
        if self.id is None:
            self.id = uuid4()

    def to_dict(self) -> dict:
        """
        Converts the transaction to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all transaction fields.
        """
        return {
            "id": str(self.id) if self.id else None,
            "description": self.description,
            "amount": str(self.amount),
            "type": self.type.value,
            "date": self.date.isoformat() if self.date else None,
        }
