"""
Transaction Serializers module.

This module contains serializers for validating and transforming
transaction data between the API and the application layer.
"""

from decimal import Decimal, InvalidOperation

from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    """
    Serializer for Transaction response.
    
    Used to serialize transaction data for API responses.
    """
    id = serializers.CharField(read_only=True)
    description = serializers.CharField()
    amount = serializers.CharField()
    type = serializers.CharField()
    date = serializers.CharField()


class TransactionCreateSerializer(serializers.Serializer):
    """
    Serializer for creating/updating a Transaction.
    
    Handles validation of input data according to business rules.
    """
    description = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Description is required.',
            'blank': 'Description cannot be blank.',
        }
    )
    amount = serializers.DecimalField(
        required=True,
        max_digits=15,
        decimal_places=2,
        min_value=Decimal('0.01'),
        error_messages={
            'required': 'Amount is required.',
            'invalid': 'Amount must be a valid number.',
            'min_value': 'Amount must be greater than zero.',
        }
    )
    type = serializers.ChoiceField(
        required=True,
        choices=['income', 'expense'],
        error_messages={
            'required': 'Type is required.',
            'invalid_choice': "Type must be 'income' or 'expense'.",
        }
    )
    date = serializers.DateField(
        required=True,
        input_formats=['%Y-%m-%d', 'iso-8601'],
        error_messages={
            'required': 'Date is required.',
            'invalid': 'Date must be in YYYY-MM-DD format.',
        }
    )


class TransactionUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating a Transaction.
    
    All fields are optional to support partial updates (PATCH).
    """
    description = serializers.CharField(
        required=False,
        allow_blank=False,
        error_messages={
            'blank': 'Description cannot be blank.',
        }
    )
    amount = serializers.DecimalField(
        required=False,
        max_digits=15,
        decimal_places=2,
        min_value=Decimal('0.01'),
        error_messages={
            'invalid': 'Amount must be a valid number.',
            'min_value': 'Amount must be greater than zero.',
        }
    )
    type = serializers.ChoiceField(
        required=False,
        choices=['income', 'expense'],
        error_messages={
            'invalid_choice': "Type must be 'income' or 'expense'.",
        }
    )
    date = serializers.DateField(
        required=False,
        input_formats=['%Y-%m-%d', 'iso-8601'],
        error_messages={
            'invalid': 'Date must be in YYYY-MM-DD format.',
        }
    )


class SummarySerializer(serializers.Serializer):
    """
    Serializer for Summary response.
    """
    total_income = serializers.CharField()
    total_expense = serializers.CharField()
    net_balance = serializers.CharField()


class PaginationMetaSerializer(serializers.Serializer):
    """
    Serializer for pagination metadata.
    """
    page = serializers.IntegerField()
    size = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    total_items = serializers.IntegerField()


class PaginationLinksSerializer(serializers.Serializer):
    """
    Serializer for pagination links.
    """
    self = serializers.CharField()
    next = serializers.CharField(allow_null=True)
    prev = serializers.CharField(allow_null=True)
    first = serializers.CharField()
    last = serializers.CharField()


class PaginatedTransactionSerializer(serializers.Serializer):
    """
    Serializer for paginated transaction response.
    """
    data = TransactionSerializer(many=True)
    meta = PaginationMetaSerializer()
    links = PaginationLinksSerializer()
