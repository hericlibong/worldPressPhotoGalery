import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class LetempsPicturesSpider(CrawlSpider):
    name = "letemps_pictures"
    allowed_domains = ["letemps.ch"]
    start_urls = ["https://www.letemps.ch/en-images"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//li[@class='featured'][1]//a"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        container = response.xpath("//figure[contains(@id, 'post-')]")
        for item in container:
            custom_items = ApipicturesItem()
            custom_items['picture'] = item.xpath(".//img/@src").get()
            caption_credit_author_element = item.xpath("./div/figcaption/p")
            caption_text = caption_credit_author_element.xpath("substring-before(text(), '©')").get()
            custom_items['caption'] = caption_text.replace('-', '').replace('\xa0', '').rstrip('— ') 
            author_credit_text = caption_credit_author_element.xpath("substring-after(text(), '©')").get()
            custom_items['author'] = author_credit_text.split('/')[0].strip()
            custom_items['credits'] = author_credit_text.split('/')[1].strip()
            custom_items['sectionTitle'] = response.xpath('//h1/text()').get()
            custom_items['pageUrl'] = response.url
            date = response.xpath("//meta[@property='og:article:published_time']/@content").get()
            custom_items['pubDate'] = date.split("T")[0]
            custom_items['media'] = response.xpath("//meta[@name='application-name']/@content").get()
            custom_items['location'] = 'Ref. to caption'
            custom_items['pictureEditor']= response.xpath("//div[@class='post__author__text']/span/a/text()").get()

            yield custom_items