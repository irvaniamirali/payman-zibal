import pytest
from zibal.models import VerifyRequest, VerifyResponse
from zibal.enums.transaction_status import TransactionStatus


@pytest.mark.asyncio
async def test_verify_payment_success(mock_zibal_gateway, mock_verify_response_success):
    mock_zibal_gateway.client.post.return_value = mock_verify_response_success
    request = VerifyRequest(track_id=123456789)

    response: VerifyResponse = await mock_zibal_gateway.verify_payment(request)
    assert isinstance(response, VerifyResponse)
    assert response.success
    assert response.already_verified
