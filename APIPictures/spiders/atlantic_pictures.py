import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class AtlanticPicturesSpider(CrawlSpider):
    name = "atlantic_pictures"
    allowed_domains = ["theatlantic.com"]
    start_urls = ["https://www.theatlantic.com/photo/categories/photos-of-the-week/"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//li[@class='grid-article grid-item three-row'][1]/a"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        container = response.xpath('//li[contains(@id, "img")]')
        for item in container:
            custom_items = ApipicturesItem() 
            custom_items['media'] = item.xpath("//meta[@property='og:site_name']/@content").get()
            custom_items['sectionTitle'] = response.xpath("substring-before(//meta[@property='og:title']/@content, ':')").get()
            custom_items['pageUrl'] = response.url
            date_string = response.xpath("//ul[@class='metadata']/li[@class='date'][1]/text()").get() 
            custom_items['pubDate'] = datetime.strptime(date_string, '%B %d, %Y').strftime('%Y-%m-%d') 
            custom_items['caption'] = item.xpath("normalize-space(.//div/p[@class='caption']/span)").get()
            author_credits_item = item.xpath(".//div//div[@class='credit']")
            custom_items['author'] = author_credits_item.xpath("substring-before(text(), '/')").get().strip()
            custom_items['credits'] = author_credits_item.xpath("substring-after(text(), '/')").get().strip()
            custom_items['picture'] = item.xpath(".//picture//img/@data-src").get()
            custom_items['location'] = 'Ref. to caption'
            custom_items['pictureEditor'] = response.xpath("//ul[@class='metadata']/li[@class='byline']/a/@title").get()
            yield custom_items
            
