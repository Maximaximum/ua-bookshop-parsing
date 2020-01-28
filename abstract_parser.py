from abc import ABC, abstractmethod
from typing import cast

from parse_results import ParseResults


class AbstractParser(ABC):
    @property
    @abstractmethod
    def HOME_URL(self):
        pass

    @property
    @abstractmethod
    def TITLE(self):
        pass

    @abstractmethod
    def get_book_stats(self) -> ParseResults:
        pass

    LANGUAGES = ('uk', 'ru')

    def empty_results(self) -> ParseResults:
        return cast(ParseResults, dict(
            map(lambda k: (k, 0), (*self.LANGUAGES, 'TOTAL'))))
