from enum import StrEnum

class BookGenre(StrEnum):
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    SCIENCE = 'Science'
    HISTORY = 'History'
    FANTASY = 'Fantasy'
    COMEDY = 'Comedy'
    DRAMA = 'Drama'

class BookLanguage(StrEnum):
    ENGLISH = 'English'
    UKRAINIAN = 'Ukrainian'
