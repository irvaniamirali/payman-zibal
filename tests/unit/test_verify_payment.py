import pytest

from zibal.models import VerifyRequest, VerifyResponse
from zibal.enums.transaction_status import TransactionStatus
from zibal.exceptions.zibal_exceptions import AlreadyConfirmedError


@pytest.mark.asyncio
async def test_verify_payment_success(zibal_gateway):
    """
    Tests a successful payment verification scenario by mocking the
    underlying HTTP client's response.
    """

    zibal_gateway.client.http_client.request.return_value = {
        "result": 100,
        "message": "success",
        "amount": 10000,
        "status": 1,
        "cardNumber": "603799******1234",
    }

    params = VerifyRequest(track_id=123456)

    response = await zibal_gateway.verify_payment(params)

    assert isinstance(response, VerifyResponse)
    assert response.success is True
    assert response.amount == 10000
    assert response.status == TransactionStatus.VERIFIED


@pytest.mark.asyncio
async def test_verify_payment_already_confirmed_api_error(zibal_gateway):
    """
    Tests failure when trying to verify an already-verified transaction,
    ensuring the correct exception is raised via the ErrorMapper.
    """

    zibal_gateway.client.http_client.request.return_value = {
        "result": 201,
        "message": "Already confirmed.",
    }

    with pytest.raises(AlreadyConfirmedError) as exc_info:
        await zibal_gateway.verify_payment(track_id=123456)

    assert str(exc_info.value) == "Already confirmed."
