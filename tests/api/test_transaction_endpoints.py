"""
Integration tests for Transaction API endpoints.

This module contains integration tests for the transaction REST API,
testing the full request/response cycle.
"""

import pytest
from decimal import Decimal
from datetime import date

from rest_framework import status


@pytest.mark.django_db
class TestCreateTransactionEndpoint:
    """Tests for POST /api/v1/transactions/"""

    def test_create_income_transaction(self, api_client, sample_transaction_data):
        """Test creating an income transaction successfully."""
        response = api_client.post(
            "/api/v1/transactions/",
            data=sample_transaction_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == sample_transaction_data["description"]
        assert response.data["amount"] == sample_transaction_data["amount"]
        assert response.data["type"] == sample_transaction_data["type"]
        assert response.data["date"] == sample_transaction_data["date"]
        assert "id" in response.data

    def test_create_expense_transaction(self, api_client, sample_expense_data):
        """Test creating an expense transaction successfully."""
        response = api_client.post(
            "/api/v1/transactions/",
            data=sample_expense_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["type"] == "expense"

    def test_create_without_description_fails(self, api_client):
        """Test that creating without description returns 400."""
        data = {
            "amount": "100.00",
            "type": "income",
            "date": "2025-01-15",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "description" in response.data

    def test_create_with_empty_description_fails(self, api_client):
        """Test that creating with empty description returns 400."""
        data = {
            "description": "",
            "amount": "100.00",
            "type": "income",
            "date": "2025-01-15",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_without_amount_fails(self, api_client):
        """Test that creating without amount returns 400."""
        data = {
            "description": "Test",
            "type": "income",
            "date": "2025-01-15",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data

    def test_create_with_zero_amount_fails(self, api_client):
        """Test that creating with zero amount returns 400."""
        data = {
            "description": "Test",
            "amount": "0.00",
            "type": "income",
            "date": "2025-01-15",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_with_negative_amount_fails(self, api_client):
        """Test that creating with negative amount returns 400."""
        data = {
            "description": "Test",
            "amount": "-100.00",
            "type": "income",
            "date": "2025-01-15",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_with_invalid_type_fails(self, api_client):
        """Test that creating with invalid type returns 400."""
        data = {
            "description": "Test",
            "amount": "100.00",
            "type": "invalid",
            "date": "2025-01-15",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_without_date_fails(self, api_client):
        """Test that creating without date returns 400."""
        data = {
            "description": "Test",
            "amount": "100.00",
            "type": "income",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "date" in response.data

    def test_create_with_invalid_date_format_fails(self, api_client):
        """Test that creating with invalid date format returns 400."""
        data = {
            "description": "Test",
            "amount": "100.00",
            "type": "income",
            "date": "15/01/2025",
        }

        response = api_client.post("/api/v1/transactions/", data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListTransactionsEndpoint:
    """Tests for GET /api/v1/transactions/"""

    def test_list_empty_transactions(self, api_client):
        """Test listing when no transactions exist."""
        response = api_client.get("/api/v1/transactions/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == []
        assert response.data["meta"]["total_items"] == 0

    def test_list_all_transactions(self, api_client, multiple_transactions):
        """Test listing all transactions."""
        response = api_client.get("/api/v1/transactions/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meta"]["total_items"] == 5

    def test_filter_by_type_income(self, api_client, multiple_transactions):
        """Test filtering transactions by income type."""
        response = api_client.get("/api/v1/transactions/?type=income")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meta"]["total_items"] == 2
        for transaction in response.data["data"]:
            assert transaction["type"] == "income"

    def test_filter_by_type_expense(self, api_client, multiple_transactions):
        """Test filtering transactions by expense type."""
        response = api_client.get("/api/v1/transactions/?type=expense")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meta"]["total_items"] == 3
        for transaction in response.data["data"]:
            assert transaction["type"] == "expense"

    def test_filter_by_description(self, api_client, multiple_transactions):
        """Test filtering transactions by description (case-insensitive)."""
        response = api_client.get("/api/v1/transactions/?description=sal")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meta"]["total_items"] == 1
        assert "Salário" in response.data["data"][0]["description"]

    def test_filter_by_description_case_insensitive(self, api_client, multiple_transactions):
        """Test that description filter is case-insensitive."""
        response = api_client.get("/api/v1/transactions/?description=SAL")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meta"]["total_items"] == 1

    def test_combine_filters(self, api_client, multiple_transactions):
        """Test combining type and description filters."""
        response = api_client.get("/api/v1/transactions/?type=expense&description=alu")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["meta"]["total_items"] == 1
        assert response.data["data"][0]["description"] == "Aluguel"

    def test_pagination(self, api_client, multiple_transactions):
        """Test pagination of transactions."""
        response = api_client.get("/api/v1/transactions/?page=1&size=2")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data["meta"]["total_items"] == 5


@pytest.mark.django_db
class TestGetTransactionEndpoint:
    """Tests for GET /api/v1/transactions/{id}/"""

    def test_get_existing_transaction(self, api_client, created_transaction):
        """Test getting an existing transaction by ID."""
        response = api_client.get(f"/api/v1/transactions/{created_transaction.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(created_transaction.id)
        assert response.data["description"] == created_transaction.description

    def test_get_nonexistent_transaction(self, api_client, db):
        """Test getting a nonexistent transaction returns 404."""
        from uuid import uuid4
        
        response = api_client.get(f"/api/v1/transactions/{uuid4()}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_with_invalid_uuid(self, api_client, db):
        """Test getting with invalid UUID returns 400."""
        response = api_client.get("/api/v1/transactions/invalid-uuid/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateTransactionEndpoint:
    """Tests for PUT/PATCH /api/v1/transactions/{id}/"""

    def test_full_update_transaction(self, api_client, created_transaction):
        """Test full update (PUT) of a transaction."""
        updated_data = {
            "description": "Salário atualizado",
            "amount": "5500.00",
            "type": "income",
            "date": "2025-01-20",
        }

        response = api_client.put(
            f"/api/v1/transactions/{created_transaction.id}/",
            data=updated_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == "Salário atualizado"
        assert response.data["amount"] == "5500.00"
        assert response.data["date"] == "2025-01-20"

    def test_partial_update_description(self, api_client, created_transaction):
        """Test partial update (PATCH) of description only."""
        response = api_client.patch(
            f"/api/v1/transactions/{created_transaction.id}/",
            data={"description": "Nova descrição"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == "Nova descrição"

    def test_partial_update_amount(self, api_client, created_transaction):
        """Test partial update (PATCH) of amount only."""
        response = api_client.patch(
            f"/api/v1/transactions/{created_transaction.id}/",
            data={"amount": "6000.00"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["amount"] == "6000.00"

    def test_update_nonexistent_transaction(self, api_client, db):
        """Test updating a nonexistent transaction returns 404."""
        from uuid import uuid4
        
        response = api_client.put(
            f"/api/v1/transactions/{uuid4()}/",
            data={
                "description": "Test",
                "amount": "100.00",
                "type": "income",
                "date": "2025-01-15",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_with_invalid_amount_fails(self, api_client, created_transaction):
        """Test that updating with invalid amount returns 400."""
        response = api_client.patch(
            f"/api/v1/transactions/{created_transaction.id}/",
            data={"amount": "-100.00"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteTransactionEndpoint:
    """Tests for DELETE /api/v1/transactions/{id}/"""

    def test_delete_existing_transaction(self, api_client, created_transaction):
        """Test deleting an existing transaction."""
        response = api_client.delete(f"/api/v1/transactions/{created_transaction.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify it's deleted
        get_response = api_client.get(f"/api/v1/transactions/{created_transaction.id}/")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_transaction(self, api_client, db):
        """Test deleting a nonexistent transaction returns 404."""
        from uuid import uuid4
        
        response = api_client.delete(f"/api/v1/transactions/{uuid4()}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestSummaryEndpoint:
    """Tests for GET /api/v1/summary/"""

    def test_summary_empty_transactions(self, api_client):
        """Test summary when no transactions exist."""
        response = api_client.get("/api/v1/summary/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_income"] == "0.00"
        assert response.data["total_expense"] == "0.00"
        assert response.data["net_balance"] == "0.00"

    def test_summary_with_transactions(self, api_client, multiple_transactions):
        """Test summary calculation with transactions."""
        response = api_client.get("/api/v1/summary/")

        assert response.status_code == status.HTTP_200_OK
        # Income: 5000 + 2000 = 7000
        assert response.data["total_income"] == "7000.00"
        # Expense: 1500 + 50 + 800 = 2350
        assert response.data["total_expense"] == "2350.00"
        # Balance: 7000 - 2350 = 4650
        assert response.data["net_balance"] == "4650.00"

    def test_summary_with_only_income(self, api_client, created_transaction):
        """Test summary with only income transactions."""
        response = api_client.get("/api/v1/summary/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_income"] == "5000.00"
        assert response.data["total_expense"] == "0.00"
        assert response.data["net_balance"] == "5000.00"

    def test_summary_with_only_expense(self, api_client, created_expense):
        """Test summary with only expense transactions."""
        response = api_client.get("/api/v1/summary/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_income"] == "0.00"
        assert response.data["total_expense"] == "1500.00"
        assert response.data["net_balance"] == "-1500.00"


@pytest.mark.django_db
class TestURLTrailingSlash:
    """Tests for URL trailing slash handling."""

    def test_create_without_trailing_slash(self, api_client, sample_transaction_data):
        """Test creating transaction without trailing slash."""
        response = api_client.post(
            "/api/v1/transactions",
            data=sample_transaction_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_list_without_trailing_slash(self, api_client, db):
        """Test listing transactions without trailing slash."""
        response = api_client.get("/api/v1/transactions")

        assert response.status_code == status.HTTP_200_OK

    def test_summary_without_trailing_slash(self, api_client, db):
        """Test summary endpoint without trailing slash."""
        response = api_client.get("/api/v1/summary")

        assert response.status_code == status.HTTP_200_OK
