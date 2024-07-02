# src/appwrite_api.py
import os
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.query import Query
from appwrite.exception import AppwriteException


__all__ = ["ID", "Query"]

# Set Your Appwrite Info
APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"
APPWRITE_PROJECT_ID = "sitemap-indexer"
if not (APPWRITE_API_KEY := os.getenv("APPWRITE_API_KEY")):
    raise ValueError("APPWRITE_API_KEY environment variable is not set")
DATABASE_ID = "66822a1b0013107744ac"
SITE_ID = "66822a35003da2e27147"

_client = Client()
_client.set_endpoint(APPWRITE_ENDPOINT)
_client.set_project(APPWRITE_PROJECT_ID)
_client.set_key(APPWRITE_API_KEY)


class AppData:
    databases = Databases(_client)

    class Id:
        DATABASE_ID = DATABASE_ID
        SITE_ID = SITE_ID

    @staticmethod
    def list_documents(collection_id: str, queries=None) -> list[dict]:
        _documents = AppData.databases.list_documents(
            database_id=AppData.Id.DATABASE_ID,
            collection_id=collection_id,
            queries=queries,
        )
        if isinstance(_documents, dict):
            documents: list[dict] = _documents.get("documents", [])
        else:
            raise AppwriteException("Api Response is not a dict")

        return documents

    @staticmethod
    def get_document(collection_id: str, document_id: str, queries=None) -> dict:
        _document = AppData.databases.get_document(
            database_id=AppData.Id.DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id,
            queries=queries,
        )
        if isinstance(_document, dict):
            document = _document
        else:
            raise AppwriteException("Api Response is not a dict")

        return document

    @staticmethod
    def update_document(
        collection_id: str, document_id: str, data: dict, permissions=None
    ) -> dict:
        _document = AppData.databases.update_document(
            database_id=AppData.Id.DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id,
            data=data,
            permissions=permissions,
        )
        if isinstance(_document, dict):
            document = _document
        else:
            raise AppwriteException("Api Response is not a dict")

        return document

    @staticmethod
    def create_document(collection_id: str, data: dict, permissions=None) -> dict:
        _document = AppData.databases.create_document(
            database_id=AppData.Id.DATABASE_ID,
            collection_id=collection_id,
            document_id=ID.unique(),
            data=data,
            permissions=permissions,
        )
        if isinstance(_document, dict):
            document = _document
        else:
            raise AppwriteException("Api Response is not a dict")

        return document

    @staticmethod
    def delete_document(collection_id: str, document_id: str) -> None:
        AppData.databases.delete_document(
            database_id=AppData.Id.DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id,
        )

        return None


class Context:
    class Request:
        def __init__(self, method, headers=None):
            self.method = method
            self.headers = headers or {}

    class Response:
        def json(self, data):
            return data

        def send(self, data):
            return data

    def __init__(self, method, headers=None):
        self.req = self.Request(method, headers)
        self.res = self.Response()

    def _print(self, level, message):
        print(f"[{level}] {message}")

    def log(self, message):
        self._print("LOG", message)

    def error(self, message):
        self._print("ERROR", message)
