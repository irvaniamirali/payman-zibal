import pytest
from unittest.mock import AsyncMock
from zibal.gateway import Zibal
from zibal.models import PaymentResponse, VerifyResponse, InquiryResponse, PaymentRequest

@pytest.fixture
def mock_zibal_gateway():
    """Return a Zibal instance with mocked HTTP client."""
    gateway = Zibal(merchant_id="test_merchant")
    gateway.client.post = AsyncMock()
    return gateway

@pytest.fixture
def mock_payment_success_response():
    return {"result": 100, "track_id": 123456789, "message": "success"}

@pytest.fixture
def mock_payment_error_response():
    return {"result": 104, "message": "Invalid merchant"}

@pytest.fixture
def mock_verify_response_success():
    return {"result": 100, "status": 1, "message": "success", "track_id": 123456789}

@pytest.fixture
def mock_inquiry_response_success():
    return {
        "result": 100,
        "status": 1,
        "amount": 1000,
        "track_id": 123456789,
        "message": "success",
        "order_id": "ORD123",
    }
