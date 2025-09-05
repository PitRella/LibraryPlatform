from abc import ABC, abstractmethod
import json

import csv
from io import StringIO
from typing import Any

from fastapi import UploadFile


class FileBookImporter(ABC):
    @abstractmethod
    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        raise NotImplementedError


class BookImporterFactory:
    @staticmethod
    def get_importer(file: UploadFile) -> FileBookImporter:
        filename: str | None = file.filename
        if not filename:
            raise ValueError("File must have a filename")
        if filename.endswith(".json"):
            return JSONBookImporter()
        elif filename.endswith(".csv"):
            return CSVBookImporter()
        else:
            raise ValueError("Unsupported file format. Use .json or .csv")


class JSONBookImporter(FileBookImporter):
    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        content = await file.read()
        data = json.loads(content.decode("utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON must contain an array of books")
        return data


class CSVBookImporter(FileBookImporter):
    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        content = await file.read()
        reader = csv.DictReader(StringIO(content.decode("utf-8")))
        return list(reader)
