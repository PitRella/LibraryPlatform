from abc import ABC, abstractmethod
from typing import Any, cast

from fastapi import UploadFile

from src.books.services.importers import JSONBookImporter, CSVBookImporter


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