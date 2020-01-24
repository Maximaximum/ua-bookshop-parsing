from parse_results import ParseResults


class Parser:
    HOME_URL = 'https://mock.ua'
    TITLE = 'Mock'

    def get_book_stats(self) -> ParseResults:
        return {
            'uk': 10,
            'ru': 5,
            'TOTAL': 100
        }
