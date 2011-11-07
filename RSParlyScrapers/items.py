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

class ResearchPaperItem(Item):
    title = Field()
    authors = Field()
    topics = Field()
    date = Field()
    note = Field()
    summary = Field()
    download = Field()

