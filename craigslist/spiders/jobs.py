# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr']

    def parse(self, response):
        #getting all the container of detail
        
        jobs=response.xpath ("//p[@class='result-info']")

        for job in jobs:
            title = job.xpath("a/text()").extract_first()
            address = job.xpath(".//span[@class='result-hood']/text()").extract_first("")[2:-1]
            relative_url = job.xpath("a[@class='result-title hdrlnk']/@href").extract_first()
            yield Request(relative_url,callback=self.parse_page,meta= {"Title":title, "Address":address,"URL":relative_url})         
     
        relative_url = response.xpath("//*[@class='button next']/@href").extract_first()
        absolute_url = response.urljoin(relative_url)
        yield Request(absolute_url,callback=self.parse)
    
    def parse_page(self,response):
        #we scrape the description in this function       
        #when descriptin is in multiple lines
        response.meta["Description"] = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())
        response.meta["Compensation"] = response.xpath('//p[@class="attrgroup"]/span/b/text()')[0].extract()
        response.meta["Employment Type"] = response.xpath('//p[@class="attrgroup"]/span/b/text()')[1].extract()  
        yield response.meta
        
     
           