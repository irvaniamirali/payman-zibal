import pytest
from zibal.models import PaymentRequest, PaymentResponse
from zibal.exceptions.zibal_exceptions import InvalidMerchantError

@pytest.mark.asyncio
async def test_initiate_payment_success(mock_zibal_gateway, mock_payment_success_response):
    mock_zibal_gateway.client.post.return_value = mock_payment_success_response

    params = PaymentRequest(amount=1000, callback_url="https://example.com/callback")
    response: PaymentResponse = await mock_zibal_gateway.initiate_payment(params)

    assert isinstance(response, PaymentResponse)
    assert response.success
    assert response.track_id == 123456789
    assert response.message == "success"
    mock_zibal_gateway.client.post.assert_awaited_once()

@pytest.mark.asyncio
async def test_initiate_payment_validation_error(mock_zibal_gateway):
    # amount < 100 should raise Pydantic validation error
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        await mock_zibal_gateway.initiate_payment(amount=50)
