from abc import ABC, abstractmethod

from fastapi import UploadFile

class FileBookImporter(ABC):
    @abstractmethod
    async def parse(self, file: UploadFile) -> list[dict]:
        raise NotImplementedError
