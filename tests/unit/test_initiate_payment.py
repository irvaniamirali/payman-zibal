import pytest
from pydantic import ValidationError

from zibal.models import PaymentRequest, PaymentResponse


@pytest.mark.asyncio
async def test_initiate_payment_success(zibal_gateway):
    """
    Tests a successful payment initiation scenario by mocking the
    underlying HTTP client's response.
    """

    zibal_gateway.client.http_client.request.return_value = {
        "result": 100,
        "trackId": 123456,
        "message": "success",
    }

    params = PaymentRequest(
        amount=10000,
        callback_url="https://example.com/callback",
    )

    response = await zibal_gateway.initiate_payment(params)

    assert isinstance(response, PaymentResponse)
    assert response.success is True
    assert response.track_id == 123456


def test_payment_request_validation_with_invalid_callback_url():
    """
    Tests that the PaymentRequest model raises ValidationError for an invalid URL.
    This is a direct unit test of the model itself.
    """

    with pytest.raises(ValidationError):
        PaymentRequest(amount=10000, callback_url="invalid-url")
