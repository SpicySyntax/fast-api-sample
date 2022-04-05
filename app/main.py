"""
REST API main module
"""
import logging
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException

from app.db.db import DynamoDbClient
from app.models.data import Item

logger = logging.getLogger(__name__)

app = FastAPI()


def dynabodb_client() -> DynamoDbClient[Item]:
    return DynamoDbClient[Item]("items", Item.key_schema(), Item.attr_defs())


@app.on_event("startup")
def startup_event():
    db_client = dynabodb_client()
    if not db_client.table_exists():
        db_client.create_table()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v2/hello")
def hello_world_v2():
    return {"Hello": "World2"}


@app.get("/items/")
def read_item(
    item_name: str,
    item_val: Decimal,
    db_client: DynamoDbClient = Depends(dynabodb_client),
) -> Item:
    item = db_client.get_item(item_name, item_val)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/")
def put_item(item: Item, db_client: DynamoDbClient = Depends(dynabodb_client)):
    db_client.put_item(item)
    logger.info("putting a new item...")
    return item
