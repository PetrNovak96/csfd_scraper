from datetime import datetime
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import os

from csfd_scraper.items import FilmItem, ParticipantItem, ParticipationItem


class CSVItemPipeline(object):

    def __init__(self):
        now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        path = './artifacts/%s' % now
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        films_file = open('%s/films.csv' % path, 'w+b')
        participants_file = open('%s/participants.csv' % path, 'w+b')
        participations_file = open('%s/participations.csv' % path, 'w+b')
        self.exports = {
            FilmItem: {
                'file': films_file,
                'exporter': CsvItemExporter(films_file)
            },
            ParticipantItem: {
                'file': participants_file,
                'exporter': CsvItemExporter(participants_file)
            },
            ParticipationItem: {
                'file': participations_file,
                'exporter': CsvItemExporter(participations_file)
            },
        }

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        for export in self.exports.values():
            export['exporter'].start_exporting()

    def spider_closed(self, spider):
        for export in self.exports.values():
            export['exporter'].finish_exporting()
            export['file'].close()

    def process_item(self, item, spider):
        self.exports[type(item)]['exporter'].export_item(item)
        return item
