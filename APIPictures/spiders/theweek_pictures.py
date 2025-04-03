from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class TheweekPicturesSpider(CrawlSpider):
    name = "theweek_pictures"
    allowed_domains = ["theweek.com"]
    start_urls = ["https://theweek.com/photos"]
    rules = (Rule(LinkExtractor(restrict_xpaths="//div[@class='listing__item listing__item--hero']//a"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        container = response.xpath("//figure[contains(@class, 'van-image-figure')]")
        for item in container:
            custom_items = ApipicturesItem()
            custom_items['media'] = item.xpath("//meta[@property='og:site_name']/@content").get()
            custom_items['sectionTitle'] = response.xpath("//meta[@property='og:title']/@content").get()
            custom_items['pageUrl'] = response.url
            pubdate_raw = response.xpath("//meta[@property='article:published_time']/@content").get()
            custom_items['pubDate'] = datetime.strptime(pubdate_raw, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d")
            custom_items["caption"] = item.xpath(".//figcaption[@class='inline-layout ']//p/text()").get()
            author_credits_item = item.xpath(".//div[@class='credit']")
            custom_items['author'] = author_credits_item.xpath("substring-before(text(), '/')").get()
            custom_items['credits'] = author_credits_item.xpath("substring-after(text(), '/')").get()
            srcset = item.xpath(".//picture/source/@srcset").get()
            custom_items['picture'] = srcset.split(", ")[0].split(" ")[0]
            custom_items['location'] = 'Ref. to caption'
            picture_editor = response.xpath("//div[@class='author-byline__author-text']//span/a[@class='link author-byline__link']/text()").get()
            custom_items['pictureEditor'] = picture_editor if picture_editor else "Unknown"
            yield custom_items
