from parse_results import ParseResults


class AbstractParser:
    HOME_URL = 'https://www.yakaboo.ua/ua/knigi.html'
    TITLE = 'Yakaboo'

    def get_book_stats(self) -> ParseResults:
        pass
