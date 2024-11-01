import scrapy


class TdnewparsSpider(scrapy.Spider):
    name = "tdnewpars"
    allowed_domains = ["tdom.info"]
    start_urls = ["https://tdom.info"]

    def parse(self, response):
        pass
