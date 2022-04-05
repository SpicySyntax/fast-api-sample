""" Pytest fixtures """

import boto3
import localstack_client.session
import pytest
from testcontainers.compose import DockerCompose

from app.db.db import DynamoDbClient
from app.models.data import Item


@pytest.fixture(scope="module")
def compose_fixture():
    compose = DockerCompose(".")
    # manuall use __enter__ and __exit__
    # instead of with DockerCompose(".") as compose: ...
    compose.__enter__()
    yield compose
    compose.__exit__(None, None, None)

@pytest.fixture
def dynamodb_fixture(compose_fixture, monkeypatch) -> DynamoDbClient[Item]: # pylint: disable=unused-argument, redefined-outer-name
    session_ls = localstack_client.session.Session()
    monkeypatch.setattr(boto3, "client", session_ls.client)
    monkeypatch.setattr(boto3, "resource", session_ls.resource)
    db_client = DynamoDbClient[Item]("items", Item.key_schema(), Item.attr_defs())
    if db_client.table_exists():
        db_client.delete_table()
    else:
        db_client.create_table()
    return db_client
