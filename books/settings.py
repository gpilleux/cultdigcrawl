# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline

BOT_NAME = 'books'

SPIDER_MODULES = ['books.spiders']
NEWSPIDER_MODULE = 'books.spiders'

ROBOTSTXT_OBEY = True
HTTPCACHE_ENABLED = True

ITEM_PIPELINES = {'build.lib.books.pipelines.CustomImageNamePipeline': 300}
IMAGES_STORE = '/home/gpilleux46/crawlers/booksbot/images'
