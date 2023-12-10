import scrapy

class Casestatus(scrapy.Spider):
    name = "CaseStatus"
    allowed_domains = ["www.casestatusext.com/"]
    start_urls = ["https://www.casestatusext.com/cases/IOE0918743038/"]

    def parse(self, response):
        cases = response.xpath('//td/a/text()').getall()
        yield {
            'cases': cases,
        }
