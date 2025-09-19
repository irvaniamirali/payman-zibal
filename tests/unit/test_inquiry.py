import pytest

from zibal.models import InquiryResponse
from zibal.exceptions import InvalidTrackIdError
from zibal.enums.transaction_status import TransactionStatus


@pytest.mark.asyncio
async def test_inquiry_success(zibal_gateway):
    """
    Tests a successful transaction inquiry by mocking the
    underlying HTTP client's response.
    """

    zibal_gateway.client.http_client.request.return_value = {
        "result": 100,
        "message": "success",
        "amount": 10000,
        "status": 1,
        "orderId": "ORD-XYZ",
        "refNumber": "1234567890",
        "description": "Test payment description",
        "wage": 500,
        "createdAt": "2025-07-18T10:00:00.000000Z",
    }

    response = await zibal_gateway.inquiry(track_id=123456)

    assert isinstance(response, InquiryResponse)
    assert response.success is True
    assert response.amount == 10000
    assert response.status == TransactionStatus.VERIFIED
    assert response.description == "Test payment description"
    assert response.wage == 500


@pytest.mark.asyncio
async def test_inquiry_not_found(zibal_gateway):
    """
    Tests inquiry for a non-existent transaction by mocking the
    underlying HTTP client's error response.
    """

    zibal_gateway.client.http_client.request.return_value = {
        "result": 203,
        "message": "Invalid track ID.",
    }

    with pytest.raises(InvalidTrackIdError) as exc_info:
        await zibal_gateway.inquiry(track_id=999999)

    assert str(exc_info.value) == "Invalid track ID."
