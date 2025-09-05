from dataclasses import dataclass, asdict


@dataclass
class ImportedBooksDTO:
    imported: int
    book_ids: list[int]

    def to_dict(self) -> dict:
        return asdict(self)
