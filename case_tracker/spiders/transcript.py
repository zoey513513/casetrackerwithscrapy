import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptSpider(CrawlSpider):
    name = "transcript"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-X"]
    # Set the download delay
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # Adjust the delay time (in seconds)
    }
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/a")), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths=("// a[@ rel='next']"))),
             )

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")
        yield {
            'title': article.xpath("./h1/text()").get(),
            # 'plot': article.xpath("./p/text()").get(),
            # 'transcript':article.xpath("./div[@class='full-script']/text()").getall(),
            # 'url': response.url,
        }

# running command: scrapy crawl transcript -o scripts.csv