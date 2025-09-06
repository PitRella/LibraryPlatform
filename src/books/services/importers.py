import csv
import json
from abc import ABC, abstractmethod
from io import StringIO
from typing import Any, ClassVar

from fastapi import UploadFile

from src.books.exceptions import (
    ImportInvalidCSVStructureException,
    ImportInvalidJSONStructureException,
    ImportMissingFilenameException,
    ImportUnsupportedFormatException,
)


class FileBookImporter(ABC):
    """Base class for file book importers."""

    @abstractmethod
    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        """Parse file and return list of dictionaries."""
        raise NotImplementedError


class BookImporterFactory:
    """Factory class for book importers."""

    @staticmethod
    def get_importer(file: UploadFile) -> FileBookImporter:
        """Return appropriate importer based on file extension."""
        filename: str | None = file.filename
        if not filename:
            raise ImportMissingFilenameException from None
        if filename.endswith('.json'):
            return JSONBookImporter()
        if filename.endswith('.csv'):
            return CSVBookImporter()
        raise ImportUnsupportedFormatException from None


class JSONBookImporter(FileBookImporter):
    """JSON file importer."""

    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        """Parse JSON file and return list of dictionaries."""
        content = await file.read()
        try:
            data = json.loads(content.decode('utf-8'))
        except Exception:
            raise ImportInvalidJSONStructureException from None
        if not isinstance(data, list):
            raise ImportInvalidJSONStructureException from None
        return data


class CSVBookImporter(FileBookImporter):
    """CSV file importer."""

    REQUIRED_HEADERS: ClassVar = {
        'title',
        'genre',
        'language',
        'published_year',
    }

    async def parse(self, file: UploadFile) -> list[dict[str, Any]]:
        """Parse CSV file and return list of dictionaries."""
        content = await file.read()
        try:
            reader = csv.DictReader(StringIO(content.decode('utf-8')))
        except Exception:
            raise ImportInvalidCSVStructureException from None
        if (
            not reader.fieldnames
            or not set(reader.fieldnames) >= self.REQUIRED_HEADERS
        ):
            raise ImportInvalidCSVStructureException from None
        return list(reader)
