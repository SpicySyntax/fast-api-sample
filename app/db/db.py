""" Dynamo Db Client """
import json
import logging
from typing import Dict, Generic, List, TypeVar

import boto3
from botocore.exceptions import ClientError

import app.config as config

logger = logging.getLogger(__name__)

T = TypeVar("T")


class DynamoDbClient(Generic[T]):
    """IoC Dynamo Db Client
    Defines a client interface over boto3 api
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html#GettingStarted.Python.03.06
    """

    def __init__(self, table_name: str, key_schema: List[Dict], attr_defs: List[Dict]):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-east-1",
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            aws_session_token=config.AWS_SESSION_TOKEN,
        )
        self.table = self.dynamodb.Table(table_name)
        self.table_name = table_name
        self.key_schema = key_schema
        self.attr_defs = attr_defs

    def create_table(self):
        self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=self.key_schema,
            AttributeDefinitions=self.attr_defs,
            BillingMode="PAY_PER_REQUEST",
        )

    def delete_table(self):
        self.table.delete()

    def table_exists(self):
        table_names = [table.name for table in self.dynamodb.tables.all()]
        return self.table_name in table_names

    def put_item(self, item: T):
        # using json.loads to ensure pydantic model is serializable
        self.table.put_item(Item=json.loads(item.json()))

    def update_item(self, key: Dict[str, str], update_expr: str, expr_attrs: Dict):
        self.table.update_item(
            Key=key,
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_attrs,
            ReturnValues="UPDATED_NEW",
        )

    def get_item(self, key: Dict) -> T:
        try:
            # Key={"name": item_name, "val": item_val}
            response = self.table.get_item(Key=key)
        except ClientError as e:
            logger.error(e.response["Error"]["Message"])
        else:
            if "Item" in response:
                return response["Item"]
            return None

    def delete_item(self, key: Dict):
        self.table.delete_item(Key=key)
