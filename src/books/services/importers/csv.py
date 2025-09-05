import csv
from io import StringIO

from src.books.services.importers.base import FileBookImporter
from fastapi import UploadFile

class CSVBookImporter(FileBookImporter):
    async def parse(self, file: UploadFile) -> list[dict]:
        content = await file.read()
        reader = csv.DictReader(StringIO(content.decode("utf-8")))
        return list(reader)
