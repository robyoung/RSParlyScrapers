# Scrapy settings for RSParlyScrapers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'RSParlyScrapers'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['RSParlyScrapers.spiders']
NEWSPIDER_MODULE = 'RSParlyScrapers.spiders'
DEFAULT_ITEM_CLASS = 'RSParlyScrapers.items.RsparlyscrapersItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

