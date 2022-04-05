""" API config """
import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "test")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", "test")
