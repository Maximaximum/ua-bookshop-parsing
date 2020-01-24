from abc import ABC, abstractmethod

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
