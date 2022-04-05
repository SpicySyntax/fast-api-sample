""" Pydantic Data Models """
from abc import ABC, abstractclassmethod, abstractmethod
from decimal import Decimal
from typing import Dict, List

from pydantic import BaseModel


class AbstractDynamoModel(ABC):
    """ Abstract class for a dynamo db model """

    @abstractclassmethod
    def attr_defs(cls) -> List[Dict]:
        pass

    @abstractclassmethod
    def key_schema(cls) -> List[Dict]:
        pass

    @abstractmethod
    def get_key(self) -> Dict:
        pass


class Item(BaseModel, AbstractDynamoModel):
    """ Data model for generic item """

    name: str
    val: Decimal

    @classmethod
    def key_schema(cls) -> List[Dict]:
        return [
            {"AttributeName": "name", "KeyType": "HASH"},  # Partition Key
            {"AttributeName": "val", "KeyType": "RANGE"},  # Range Key
        ]

    @classmethod
    def attr_defs(cls) -> List[Dict]:
        return [
            {"AttributeName": "name", "AttributeType": "S"},
            {"AttributeName": "val", "AttributeType": "N"},
        ]

    # def get
    def get_key(self) -> Dict:
        return {"name": self.name, "val": self.val}
