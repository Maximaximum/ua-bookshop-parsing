import glob
import importlib
import ntpath
from site_parse_results import SiteParseResults
from abstract_parser import AbstractParser
from overall_parse_results import OverallParseResults
from typing import cast


stores = glob.glob('./stores/*.py')
imported_classes = map(
    lambda store: importlib.import_module(
        'stores.' + ntpath.basename(store)[:-3], 'stores'
    ).__getattribute__('Parser'), stores
)

overall_stats: OverallParseResults = []

for c in imported_classes:
    p = cast(AbstractParser, c())
    print('Парсимо', c.TITLE, '...')
    stats: SiteParseResults = {'title': c.TITLE, 'url': c.HOME_URL, **p.get_book_stats()}
    overall_stats.append(stats)

# Output to csv
print(overall_stats)
