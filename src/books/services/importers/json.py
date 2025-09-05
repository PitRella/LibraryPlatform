import json

from src.books.services.importers.base import FileBookImporter
from fastapi import UploadFile


class JSONBookImporter(FileBookImporter):
    async def parse(self, file: UploadFile) -> list[dict]:
        content = await file.read()
        data = json.loads(content.decode("utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON must contain an array of books")
        return data
