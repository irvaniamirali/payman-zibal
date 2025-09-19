import pytest
from unittest.mock import AsyncMock

from payman.core.http.client import AsyncHttpClient
from zibal.gateway import Zibal


@pytest.fixture
def mock_http_client():
    return AsyncMock(spec=AsyncHttpClient)


@pytest.fixture
def zibal_gateway(mock_http_client):
    zibal_instance = Zibal(merchant_id="test-merchant", http_client=mock_http_client)
    return zibal_instance
