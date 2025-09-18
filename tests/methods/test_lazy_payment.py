import pytest
from zibal.models import PaymentRequest, PaymentResponse


@pytest.mark.asyncio
async def test_lazy_payment_success(mock_zibal_gateway, mock_payment_success_response):
    mock_zibal_gateway.client.post.return_value = mock_payment_success_response
    params = PaymentRequest(amount=5000, callback_url="https://example.com")

    response: PaymentResponse = await mock_zibal_gateway.lazy_payment(params)

    assert isinstance(response, PaymentResponse)
    assert response.success
    assert response.track_id == 123456789
