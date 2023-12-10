import scrapy

class Casestatus(scrapy.Spider):
    name = "CaseStatus"
    allowed_domains = ["casestatusext.com"]
    start_urls = ["https://www.casestatusext.com/cases/IOE0918743038/"]

    def parse(self, response):
        cases = response.xpath('//td/a')

        for case in cases:
            casename = case.xpath(".//text()").get()
            relativelink = case.xpath(".//@href").get()
            yield response.follow(url=relativelink, callback=self.parse_case, meta={'casename': casename})

    def parse_case(self, response):
        casename = response.request.meta['casename']
        timelines = response.xpath('//ul[contains(@class,"ant-timeline")]/li')
        yield {
            'casename': casename,
        }
        for timeline in timelines:
            time = timeline.xpath('.//div[@class="ant-timeline-item-label"]/text()').get()
            status = timeline.xpath('.//div[@class="ant-timeline-item-content"]/text()').get()
            yield {
                'time': time, 'status': status,
            }


