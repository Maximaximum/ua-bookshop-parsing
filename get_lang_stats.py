import glob
import importlib
import ntpath

stores = glob.glob('./stores/*.py')
imported_classes = map(
    lambda store: importlib.import_module(
        'stores.' + ntpath.basename(store)[:-3], 'stores'
    ).__getattribute__('Parser'), stores
)

for c in imported_classes:
    p = c()
    print('Парсимо', c.TITLE, '...')
    print(p.get_book_stats())
