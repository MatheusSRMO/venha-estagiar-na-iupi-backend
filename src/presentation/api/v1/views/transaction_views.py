"""
Transaction Views module.

This module contains the API views for transaction endpoints.
Views are thin controllers that delegate business logic to use cases.
"""

from uuid import UUID

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from src.application.dtos import CreateTransactionDTO, UpdateTransactionDTO
from src.application.use_cases import (
    CreateTransactionUseCase,
    GetTransactionUseCase,
    ListTransactionsUseCase,
    UpdateTransactionUseCase,
    DeleteTransactionUseCase,
    GetSummaryUseCase,
)
from src.infrastructure.django_app.repositories import DjangoTransactionRepository
from src.presentation.api.v1.serializers.transaction_serializer import (
    TransactionSerializer,
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
    SummarySerializer,
    PaginatedTransactionSerializer,
)


def get_repository():
    """
    Factory function to get the transaction repository.
    
    This function can be modified to return different repository
    implementations for testing or when switching frameworks.
    
    Returns:
        TransactionRepositoryInterface: The repository implementation.
    """
    return DjangoTransactionRepository()


class TransactionViewSet(ViewSet):
    """
    ViewSet for Transaction CRUD operations.
    
    This ViewSet provides the following endpoints:
    - POST /transactions/ - Create a new transaction
    - GET /transactions/ - List all transactions (with optional filters)
    - GET /transactions/{id}/ - Get a specific transaction
    - PUT /transactions/{id}/ - Update a transaction
    - PATCH /transactions/{id}/ - Partially update a transaction
    - DELETE /transactions/{id}/ - Delete a transaction
    """

    def create(self, request):
        """
        Creates a new transaction.
        
        Args:
            request: The HTTP request with transaction data.
            
        Returns:
            Response: The created transaction or validation errors.
        """
        serializer = TransactionCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            dto = CreateTransactionDTO(
                description=serializer.validated_data['description'],
                amount=serializer.validated_data['amount'],
                type=serializer.validated_data['type'],
                date=serializer.validated_data['date'],
            )

            use_case = CreateTransactionUseCase(get_repository())
            result = use_case.execute(dto)

            response_serializer = TransactionSerializer(result.__dict__)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request):
        """
        Lists all transactions with optional filters and pagination.
        
        Query Parameters:
            description: Filter by description (case-insensitive partial match).
            type: Filter by transaction type ('income' or 'expense').
            page: Page number (1-indexed, defaults to 1).
            size: Number of items per page (defaults to 10, max 100).
            
        Args:
            request: The HTTP request with optional query parameters.
            
        Returns:
            Response: Paginated list of transactions matching the filters.
        """
        description = request.query_params.get('description')
        transaction_type = request.query_params.get('type')
        
        try:
            page = int(request.query_params.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        
        try:
            size = int(request.query_params.get('size', 10))
        except (ValueError, TypeError):
            size = 10

        use_case = ListTransactionsUseCase(get_repository())
        result = use_case.execute(
            description=description,
            transaction_type=transaction_type,
            page=page,
            size=size,
            base_url=request.path,
        )

        response_data = {
            'data': [item.__dict__ for item in result.data],
            'meta': result.meta.__dict__,
            'links': result.links.__dict__,
        }
        serializer = PaginatedTransactionSerializer(response_data)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieves a specific transaction by ID.
        
        Args:
            request: The HTTP request.
            pk: The transaction ID (UUID).
            
        Returns:
            Response: The transaction or 404 if not found.
        """
        try:
            transaction_id = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid transaction ID format.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = GetTransactionUseCase(get_repository())
        result = use_case.execute(transaction_id)

        if result is None:
            return Response(
                {'error': 'Transaction not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TransactionSerializer(result.__dict__)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        Updates a transaction (full update).
        
        Args:
            request: The HTTP request with transaction data.
            pk: The transaction ID (UUID).
            
        Returns:
            Response: The updated transaction or errors.
        """
        return self._update_transaction(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        """
        Partially updates a transaction.
        
        Args:
            request: The HTTP request with partial transaction data.
            pk: The transaction ID (UUID).
            
        Returns:
            Response: The updated transaction or errors.
        """
        return self._update_transaction(request, pk, partial=True)

    def _update_transaction(self, request, pk, partial=False):
        """
        Internal method to handle transaction updates.
        
        Args:
            request: The HTTP request.
            pk: The transaction ID.
            partial: Whether this is a partial update.
            
        Returns:
            Response: The updated transaction or errors.
        """
        try:
            transaction_id = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid transaction ID format.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if partial:
            serializer = TransactionUpdateSerializer(data=request.data)
        else:
            serializer = TransactionCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            dto = UpdateTransactionDTO(
                description=serializer.validated_data.get('description'),
                amount=serializer.validated_data.get('amount'),
                type=serializer.validated_data.get('type'),
                date=serializer.validated_data.get('date'),
            )

            use_case = UpdateTransactionUseCase(get_repository())
            result = use_case.execute(transaction_id, dto)

            if result is None:
                return Response(
                    {'error': 'Transaction not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            response_serializer = TransactionSerializer(result.__dict__)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None):
        """
        Deletes a transaction.
        
        Args:
            request: The HTTP request.
            pk: The transaction ID (UUID).
            
        Returns:
            Response: Empty response with 204 status or 404 if not found.
        """
        try:
            transaction_id = UUID(pk)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid transaction ID format.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = DeleteTransactionUseCase(get_repository())
        deleted = use_case.execute(transaction_id)

        if not deleted:
            return Response(
                {'error': 'Transaction not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class SummaryView(APIView):
    """
    API View for financial summary.
    
    Provides an endpoint to get the total income, expense, and net balance.
    """

    def get(self, request):
        """
        Gets the financial summary.
        
        Args:
            request: The HTTP request.
            
        Returns:
            Response: The financial summary.
        """
        use_case = GetSummaryUseCase(get_repository())
        result = use_case.execute()

        serializer = SummarySerializer(result.__dict__)
        return Response(serializer.data, status=status.HTTP_200_OK)
