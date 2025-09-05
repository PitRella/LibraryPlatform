from enum import StrEnum

class BookGenre(StrEnum):
    FICTION = 'FICTION'
    NON_FICTION = 'NON_FICTION'
    SCIENCE = 'SCIENCE'
    HISTORY = 'HISTORY'
    FANTASY = 'FANTASY'
    COMEDY = 'COMEDY'
    DRAMA = 'DRAMA'

class BookLanguage(StrEnum):
    ENGLISH = 'ENGLISH'
    UKRAINIAN = 'UKRAINIAN'
