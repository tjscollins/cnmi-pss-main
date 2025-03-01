# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import requests
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from crawler.spiders.image_spider import ImageSpider
from crawler.spiders.links_spider import LinkSpider

SETTINGS = get_project_settings()


class DuplicateImagesPipeline(object):

    def __init__(self):
        self.sources_seen = set()

    def process_item(self, item, spider):
        new_sources = []
        drop = True
        for source in item['sources']:
            if source not in self.sources_seen:
                self.sources_seen.add(source)
                new_sources.append(source)
                drop = False
        item['sources'] = new_sources
        if drop:
            raise DropItem('No new image sources found: %s' % item)
        else:
            return item


class CheckImageStatusPipeline(object):

    def process_item(self, item, spider):
        item_sources = []
        for source in item['sources']:
            print('Checking image at: ', source)
            response = requests.head(source)
            item_sources.append(
                {'url': source, 'status': response.status_code})

        item['sources'] = item_sources
        return item

class CheckLinkStatusPipeline(object):

    def process_item(self, item, spider):
        links = []
        for link in item['links']:
            print('Checking link at: ', link)
            response = requests.head(link)
            if response.status_code in range(300, 400):
                response = requests.head(response.headers['Location'])
            links.append(
                {'url': link, 'status': response.status_code})

        item['links'] = links
        return item


class DuplicateLinksPipeline(object):

    def __init__(self):
        self.links_seen = set()

    def process_item(self, item, spider):
        new_links = []
        drop = True
        for link in item['links']:
            if link not in self.links_seen:
                self.links_seen.add(link)
                new_links.append(link)
                drop = False
        item['links'] = new_links
        if drop:
            raise DropItem('No new links found: %s' % item)
        else:
            return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        if isinstance(spider, LinkSpider):
            self.file = open(SETTINGS['LINK_DATA'], 'w')
        elif isinstance(spider, ImageSpider):
            self.file = open(SETTINGS['IMG_DATA'], 'w')
        else:
            raise Exception('Unknown spider class ' + str(spider))

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
