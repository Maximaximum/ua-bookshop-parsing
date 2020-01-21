import requests
from pyquery import PyQuery as pq


class Parser:
    LANG_QUERY_PARAM_VALUES = {
        'uk': 'Ukrainskij',
        'ru': 'Russkij'
    }
    URL = 'https://www.yakaboo.ua/ua/knigi.html'
    TITLE = 'Yakaboo'

    def get_book_stats(self):
        response = requests.get(self.URL)
        html = pq(response.text)
        menu_items = html(
            'aside .block-categories-list .title'
        ).filter(lambda i, title: title.text == 'Розділи').closest(
            '.block-categories-list'
        ).find('.block-content>ul>li:not(.item_stock)>a')

        languages = ['uk', 'ru']

        for cat_url in map(lambda item: pq(item).attr('href'), menu_items):
            section_results = {}
            for lang in languages:
                section_results[lang] = self.parse_category(cat_url, lang)
            print(cat_url, section_results)

    def parse_category(self, url, lang_code):
        url += '?book_lang={}'.format(self.LANG_QUERY_PARAM_VALUES[lang_code])
        response = requests.get(url)
        html = pq(response.text)

        books_on_one_page = len(html('.products-grid li'))

        # get pagination
        last_page_anchor = html('.pagination ul li a.last')

        if not last_page_anchor:
            last_page_anchor = pq(html(
                '.pagination ul li.paginator_page a')[-1])

        last_page_url = last_page_anchor.attr('href')
        last_page_index = int(last_page_anchor.text()) - 1

        products_on_first_page = self._count_items_on_page(html)

        if last_page_index == 0:
            total_products_in_uk = products_on_first_page
        else:
            last_page_html = pq(requests.get(url).text)
            total_products_in_uk = self._count_items_on_page(
                last_page_html) + last_page_index * products_on_first_page

        return total_products_in_uk

    def _count_items_on_page(self, html):
        return len(html('#products .item'))
