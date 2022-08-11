import csv
import datetime as dt

from constants import BASE_DIR, DATETIME_FORMAT, PEP_TABLE


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_sum = {}
        self.total_peps = 0
        self.results = PEP_TABLE

    def process_item(self, item, spider):
        self.total_peps += 1
        status = item['status']
        if status in self.status_sum:
            self.status_sum[status] += 1
        if status not in self.status_sum:
            self.status_sum[status] = 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.utcnow().strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now}.csv'
        file_path = results_dir / file_name

        for status in self.status_sum:
            self.results.append((status, self.status_sum[status]))
        self.results.append(('Total', self.total_peps))

        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(self.results)
