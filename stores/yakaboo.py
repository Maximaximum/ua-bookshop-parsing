import requests
from pyquery import PyQuery as pq


class Parser:
    LANG_QUERY_PARAM_VALUES = {
        'uk': 'Ukrainskij',
        'ru': 'Russkij'
    }
    URL = 'https://www.yakaboo.ua/ua/knigi.html'
    TITLE = 'Yakaboo'
    LANGUAGES = ('uk', 'ru')

    def get_book_stats(self) -> dict:
        response = requests.get(self.URL)
        html = pq(response.text)
        return self.get_stats_from_page_subcategories(html)

    def get_stats_from_page_subcategories(self, html: pq) -> dict:
        menu_items = self.get_categories_from_menu(html)

        total_results = dict(map(lambda k: (k, 0), self.LANGUAGES))

        for cat_url in map(lambda item: pq(item).attr('href'), menu_items):
            section_results = self.parse_category(cat_url)
            print(cat_url, section_results)
            for lang, section_result in section_results.items():
                total_results[lang] += section_result
        return total_results

    def get_categories_from_menu(self, html: pq) -> pq:
        return html(
            'aside .block-categories-list .title'
        ).filter(lambda i, title: title.text == 'Розділи').closest(
            '.block-categories-list'
        ).find('.block-content>ul>li:not(.item_stock)>a')

    def parse_category(self, url) -> dict:
        if url == 'https://www.yakaboo.ua/ua/knigi/knigi-na-inostrannyh-jazykah.html':
            return {'uk': 0, 'ru': 0}

        if url == 'https://www.yakaboo.ua/ua/knigi/izuchenie-jazykov-mira.html':
            return self.get_stats_from_page_subcategories(pq(requests.get(url).text))

        result = {}

        for lang_code in self.LANGUAGES:
            url += '?book_lang={}'.format(
                self.LANG_QUERY_PARAM_VALUES[lang_code])
            response = requests.get(url)
            html = pq(response.text)

            books_on_one_page = len(html('.products-grid li'))

            last_page = self._get_last_page(html, url)

            products_on_first_page = self._count_items_on_page(html)

            if last_page['index'] == 0:
                total_products_in_lang = products_on_first_page
            else:
                last_page_html = pq(requests.get(last_page['url']).text)
                total_products_in_lang = self._count_items_on_page(
                    last_page_html) + last_page['index'] * products_on_first_page

            result[lang_code] = total_products_in_lang
        return result

    def _count_items_on_page(self, html) -> int:
        return len(html('#products .item'))

    def _get_last_page(self, html, url) -> dict:
        # get pagination
        last_page_anchor = html('.pagination ul li a.last')

        if last_page_anchor:
            # take the hidden 'last page' anchor, if present
            return {'url': last_page_anchor.attr('href'), 'index': int(last_page_anchor.text()) - 1}
        else:
            # if the 'last page' anchor not present, check if pagination is present at all
            page_anchors = html('.pagination ul li.paginator_page a')

            if page_anchors:
                # if present - take the last visible page anchor
                last_page_anchor = pq(page_anchors[-1])
                return {'url': last_page_anchor.attr('href'), 'index': int(last_page_anchor.text()) - 1}
            else:
                # otherwise, there's only 1 page for this categoty
                return {'url': url, 'index': 0}
