""" Test Local API """
import logging
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient
from starlette.exceptions import HTTPException

from app.db.db import DynamoDbClient
from app.main import app, read_item
from app.models.data import Item

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
    logger.info("Response Matches")

def test_read_item_returns_nothing_throws_not_found():
    # Arrange
    db_client = DynamoDbClient("items", Item.key_schema(), Item.attr_defs())
    db_client.get_item = MagicMock(return_value=None)

    # Act
    try:
        read_item("test", 0.1, db_client)
    except HTTPException as e:
        # Assert
        assert e.status_code == 404
        return
    assert False

def test_read_item_returns_item():
    # Arrange
    db_client = DynamoDbClient("items", Item.key_schema(), Item.attr_defs())
    db_client.get_item = MagicMock(return_value=Item(name="test", val=1.9))

    # Act
    item = read_item("test", 0.1, db_client)

    # Assert
    assert item
