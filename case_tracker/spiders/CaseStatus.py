import time
import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

class CaseStatus(scrapy.Spider):
    name = "CaseStatus"
    allowed_domains = ["casestatusext.com"]
    start_urls = ["https://www.casestatusext.com/cases/IOE0918743038/"]

    def __init__(self, *args, **kwargs):
        super(CaseStatus, self).__init__(*args, **kwargs)
        self.driver = self.create_headless_chrome()


    def create_headless_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        with open('allcases.txt', 'w') as file_all:
            file_all.write('')
        yield from self.scrape_page(response)
        while True:
            try:
                # Find and click the "Next Page" button using Selenium
                next_button = self.driver.find_element(By.XPATH, '//li[@title="Next Page"]')
                if next_button.get_attribute("aria-disabled") == "true":
                    break  # Exit the loop if the button is disabled
                next_button.click()
                time.sleep(25)  # Allow time for the next page to load

                # Scrape data from the current page
                new_response = scrapy.http.TextResponse(
                    url=self.driver.current_url,
                    body=self.driver.page_source,
                    encoding='utf-8'
                )
                yield from self.scrape_page(new_response)
            except Exception as e:
                print(f"Error while navigating to the next page: {e}")
                break

        self.driver.quit()
        file_all.close()

    def scrape_page(self, response):
        for case in response.xpath('//td/a'):
            casename = case.xpath(".//text()").get()
            relativelink = case.xpath(".//@href").get()
            time.sleep(3)
            yield response.follow(url=relativelink, callback=self.parse_case, meta={'casename': casename})

    def parse_case(self, response):
        FileName = 'allcases.txt'
        casename = response.request.meta['casename']
        timelines = response.xpath('//ul[contains(@class,"ant-timeline")]/li')
        with open(FileName, 'a') as file:
            file.write(casename + '\n')
            for timeline in timelines:
                time = timeline.xpath('.//div[@class="ant-timeline-item-label"]/text()').get()
                status = timeline.xpath('.//div[@class="ant-timeline-item-content"]/text()').get()
                file.write(time + status + '\n')

    def wait_for_element(self, xpath, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def click_element(self, xpath):
        self.driver.find_element(By.XPATH, xpath).click()
