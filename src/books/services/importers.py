import csv
import json
from abc import ABC, abstractmethod
from io import StringIO
from typing import Any

from fastapi import UploadFile

from src.books.exceptions import (
    ImportInvalidCSVStructureException,
    ImportInvalidJSONStructureException,
    ImportMissingFilenameException,
    ImportUnsupportedFormatException,
)


class FileBookImporter(ABC):
    @abstractmethod
    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        raise NotImplementedError


class BookImporterFactory:
    @staticmethod
    def get_importer(file: UploadFile) -> FileBookImporter:
        filename: str | None = file.filename
        if not filename:
            raise ImportMissingFilenameException()
        if filename.endswith('.json'):
            return JSONBookImporter()
        if filename.endswith('.csv'):
            return CSVBookImporter()
        raise ImportUnsupportedFormatException()


class JSONBookImporter(FileBookImporter):
    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        content = await file.read()
        try:
            data = json.loads(content.decode('utf-8'))
        except Exception:
            raise ImportInvalidJSONStructureException()
        if not isinstance(data, list):
            raise ImportInvalidJSONStructureException()
        return data


class CSVBookImporter(FileBookImporter):
    REQUIRED_HEADERS = {'title', 'genre', 'language', 'published_year'}

    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        content = await file.read()
        try:
            reader = csv.DictReader(StringIO(content.decode('utf-8')))
        except Exception:
            raise ImportInvalidCSVStructureException()
        if (
            not reader.fieldnames
            or not set(reader.fieldnames) >= self.REQUIRED_HEADERS
        ):
            raise ImportInvalidCSVStructureException()
        return list(reader)
