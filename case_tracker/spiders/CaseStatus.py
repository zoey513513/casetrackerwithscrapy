import scrapy

class Casestatus(scrapy.Spider):
    name = "CaseStatus"
    allowed_domains = ["www.casestatusext.com/"]
    start_urls = ["https://www.casestatusext.com/cases/IOE0918743038/"]

    def parse(self, response):
        cases = response.xpath('//td/a')
        casenames = []
        links = []
        for case in cases:
            casename = case.xpath(".//text()").get()
            casenames.append(casename)
            relativelink = case.xpath(".//@href").get()

            # # method 1:
            # absolutelink = response.urljoin(relativelink)
            # # method 2:
            # absolutelink = f'https://www.casestatusext.com/{relativelink}'
            # method 3:
            absolutelink = response.follow(relativelink)

            links.append(absolutelink)
        yield {
            'casenames': casenames,
            'links': links,
        }
