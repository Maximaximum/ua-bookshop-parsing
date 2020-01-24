import csv
import time
import os

from overall_parse_results import OverallParseResults


class ParseResultsCsvWriter:
    DIR = './output'

    def write(self, data: OverallParseResults):
        dirname = os.path.dirname(self.DIR)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open('{}/book-languages-{}.csv'.format(self.DIR, time.strftime("%Y%m%d-%H%M%S")), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([
                'Назва книгарні',
                'URL',
                'Книжок українською',
                'Книжок російською',
                'Книжок іншими мовами',
                'Всього книжок'
            ])

            for s in data:
                writer.writerow([
                    s['title'],
                    s['home_url'],
                    s['uk'],
                    s['ru'],
                    'Н/Д',  # TODO?
                    s['TOTAL']
                ])
