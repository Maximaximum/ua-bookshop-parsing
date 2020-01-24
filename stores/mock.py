from parse_results import ParseResults

from abstract_parser import AbstractParser


class Parser(AbstractParser):
    @property
    def HOME_URL(self):
        return 'https://mock.ua'

    @property
    def TITLE(self):
        return 'Mock'

    def get_book_stats(self) -> ParseResults:
        return {
            'uk': 10,
            'ru': 5,
            'TOTAL': 100
        }
