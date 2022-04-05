""" Test Local API """
import logging
from decimal import Decimal

import pytest

from app.models.data import Item

logger = logging.getLogger(__name__)


@pytest.mark.integtest
def test_db_put(dynamodb_fixture):
    # Arrange
    db_client = dynamodb_fixture
    item = Item(name="test", val=Decimal(1.0))
    # Act
    db_client.put_item(item)
    # Assert
    assert db_client.get_item(item.get_key())
