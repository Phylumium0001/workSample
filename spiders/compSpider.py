import scrapy
from workSample.items import Workitem

class CompspiderSpider(scrapy.Spider):
    name = "compSpider"
    allowed_domains = ["1800d2c.com"]
    start_urls = ["https://www.1800d2c.com/all-brands?0dc819aa_page=1"]

    def parse(self, response):
        links = response.css('div.cardbrand.w-dyn-item')

        for link in links: 
            relativeUrl = link.css('a.cardlinkwrap.w-inline-block::attr(href)').get()
            comp_url = 'https://www.1800d2c.com' + relativeUrl

            yield response.follow(comp_url, callback=self.get_info)

        next_page = response.css('a.w-pagination-next.bpagination::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.1800d2c.com/all-brands' + next_page  

            yield response.follow(next_page_url, callback=self.parse)


    def get_info(self, response):
        workitem = Workitem()
        workitem['name'] = response.css('h1.heroh1::text').get()
        workitem['website'] = response.css('a.bxl.w-button').attrib['href']

        yield workitem