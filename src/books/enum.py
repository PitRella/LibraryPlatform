from enum import StrEnum


class BookGenre(StrEnum):
    """
    Enumeration of book genres.

    Attributes:
        FICTION: Fiction books.
        NON_FICTION: Non-fiction books.
        SCIENCE: Scientific books.
        HISTORY: Historical books.
        FANTASY: Fantasy books.
        COMEDY: Comedy books.
        DRAMA: Drama books.
    """
    FICTION = 'FICTION'
    NON_FICTION = 'NON_FICTION'
    SCIENCE = 'SCIENCE'
    HISTORY = 'HISTORY'
    FANTASY = 'FANTASY'
    COMEDY = 'COMEDY'
    DRAMA = 'DRAMA'


class BookLanguage(StrEnum):
    """
    Enumeration of supported book languages.

    Attributes:
        ENGLISH: English language.
        UKRAINIAN: Ukrainian language.
    """
    ENGLISH = 'ENGLISH'
    UKRAINIAN = 'UKRAINIAN'
