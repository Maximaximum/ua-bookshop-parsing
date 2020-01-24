import requests
from pyquery import PyQuery as pq
from typing import Union, cast
from parse_results import ParseResults


class Parser:
    LANG_QUERY_PARAM_VALUES = {
        'uk': 'Ukrainskij',
        'ru': 'Russkij'
    }
    HOME_URL = 'https://www.yakaboo.ua/ua/knigi.html'
    TITLE = 'Yakaboo'
    LANGUAGES = ('uk', 'ru')

    def get_book_stats(self) -> ParseResults:
        response = requests.get(self.HOME_URL)
        html = pq(response.text)
        return self.get_stats_from_page_subcategories(html)

    def get_stats_from_page_subcategories(self, html: pq) -> ParseResults:
        menu_items = self.get_categories_from_menu(html)

        total_results = self._empty_results()

        for cat_url in map(lambda item: pq(item).attr('href'), menu_items):
            section_results = self.parse_category(cat_url)
            print(cat_url, section_results)
            for lang, section_result in section_results.items():
                total_results[lang] += section_result  # type: ignore
        return total_results

    def get_categories_from_menu(self, html: pq) -> pq:
        return html(
            'aside .block-categories-list .title'
        ).filter(lambda i, title: title.text == 'Розділи').closest(
            '.block-categories-list'
        ).find('.block-content>ul>li:not(.item_stock)>a')

    def parse_category(self, url) -> ParseResults:
        if url == 'https://www.yakaboo.ua/ua/knigi/knigi-na-inostrannyh-jazykah.html':
            # Ignore this url - we don't want to calulate books there; they're included into other sections
            return self._empty_results()

        if url == 'https://www.yakaboo.ua/ua/knigi/izuchenie-jazykov-mira.html':
            # It's a special case category - it only contains subcategories, so parse them
            return self.get_stats_from_page_subcategories(pq(requests.get(url).text))

        result = cast(
            ParseResults,
            dict(map(lambda lang_code: (
                lang_code, self.parse_category_for_lang(url, lang_code)
            ), self.LANGUAGES))
        )

        result['TOTAL'] = self.parse_category_for_lang(
            url, None)

        return result

    def parse_category_for_lang(self, url, lang_code: Union[str, None]):
        if lang_code is not None:
            url += '?book_lang={}'.format(
                self.LANG_QUERY_PARAM_VALUES[lang_code])
        response = requests.get(url)
        html = pq(response.text)

        last_page = self._get_last_page(html, url)

        products_on_first_page = self._count_items_on_page(html)

        if last_page['index'] == 0:
            total_products_in_lang = products_on_first_page
        else:
            last_page_html = pq(requests.get(last_page['url']).text)
            total_products_in_lang = self._count_items_on_page(
                last_page_html) + last_page['index'] * products_on_first_page

        return total_products_in_lang

    def _count_items_on_page(self, html) -> int:
        return len(html('#products .item'))

    def _get_last_page(self, html, url) -> dict:
        # get pagination
        last_page_anchor = html('.pagination ul li a.last')

        if last_page_anchor:
            # take the hidden 'last page' anchor, if present
            return {
                'url': last_page_anchor.attr('href'),
                'index': int(last_page_anchor.text()) - 1
            }
        else:
            # if the 'last page' anchor not present, check if pagination is present at all
            page_anchors = html('.pagination ul li.paginator_page a')

            if page_anchors:
                # if present - take the last visible page anchor
                last_page_anchor = pq(page_anchors[-1])
                return {
                    'url': last_page_anchor.attr('href'),
                    'index': int(last_page_anchor.text()) - 1
                }
            else:
                # otherwise, there's only 1 page for this categoty
                return {'url': url, 'index': 0}

    def _empty_results(self) -> ParseResults:
        return cast(ParseResults, dict(
            map(lambda k: (k, 0), (*self.LANGUAGES, 'TOTAL'))))
