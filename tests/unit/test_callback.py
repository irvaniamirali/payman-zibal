import pytest

from zibal.models import VerifyResponse
from zibal.enums.transaction_status import TransactionStatus


@pytest.mark.asyncio
async def test_callback_verify_success(zibal_gateway):
    """
    Tests a successful server-to-server callback verification by
    mocking the underlying HTTP client's response.
    """

    callback_payload = {
        "success": 1,
        "trackId": 789012,
        "orderId": "ORD-123",
        "status": 1,
    }

    zibal_gateway.client.http_client.request.return_value = {
        "result": 100,
        "message": "Success",
        "amount": 25000,
        "status": 1,
        "trackId": 789012,
    }

    response = await zibal_gateway.callback_verify(callback=callback_payload)

    assert isinstance(response, VerifyResponse)
    assert response.success is True
    assert response.amount == 25000
    assert response.status == TransactionStatus.VERIFIED


@pytest.mark.asyncio
async def test_callback_verify_unsuccessful_status(zibal_gateway):
    """
    Tests the scenario where the callback itself indicates an
    unsuccessful payment (e.g., canceled by user).
    """

    callback_payload = {
        "success": 0,
        "trackId": 789012,
        "orderId": "ORD-123",
        "status": 3,  # Canceled by user
    }

    zibal_gateway.client.http_client.request.return_value = {
        "result": 100,
        "message": "Success",
        "amount": None,
        "status": 3,
        "trackId": 789012,
    }

    response = await zibal_gateway.callback_verify(callback=callback_payload)

    assert response.success is True
    assert response.status == TransactionStatus.CANCELED_BY_USER
    assert response.amount is None
