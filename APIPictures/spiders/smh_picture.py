from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class SmhPictureSpider(CrawlSpider):
    name = 'smh_picture'
    allowed_domains = ['smh.com.au']
    start_urls = ['https://www.smh.com.au/topic/photography-1msm']
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='_2XVos']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        container = response.xpath("//figure[@class='_2gw9I _26GFc']")
        for item in container:
            custom_items = ApipicturesItem()
            custom_items['media'] = response.xpath("//div[@class='_3uPYr _2qnYw']//h2/text()").get()
            custom_items['sectionTitle'] = response.xpath("//title/text()").get()
            date_element = response.xpath("//time[@class='_2_zR-']")
            date = date_element.xpath("substring-before(text(), '—')").get().strip()
            custom_items['pubDate'] = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
            custom_items['location'] = 'Ref. to caption'
            custom_items['pageUrl'] = response.url
            custom_items['caption'] = item.xpath(".//p[2]/span/text()").get()
            credit_string = item.xpath(".//cite/span[contains(text(), 'Credit:')]/following-sibling::text()").get()
            custom_items['credits'] = credit_string.split('/')[-1]
            author_item = item.xpath(".//p[2]/cite")
            try:
                author = author_item.xpath("substring-before(text(), '/')").get().strip()
            except AttributeError:
                author = item.xpath(".//p[2]/cite/text()").get()
            custom_items['author'] = author if author is not None else ''
            image_srcset = item.xpath(".//picture/source/@srcset").get().replace(' 2x', '')
            image_urls = image_srcset.split(", ")
            image = image_urls[1].split(" ")[0]
            custom_items['picture'] = image
            custom_items['pictureEditor'] = 'undefined'
            yield custom_items
