# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BillItem(Item):
    name = Field()
    url = Field()
    agents = Field()
    next_event = Field()
    summary = Field()
