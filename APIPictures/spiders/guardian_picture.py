from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class GuardianPictureSpider(CrawlSpider):
    name = 'guardian_picture'
    allowed_domains = ['theguardian.com']
    start_urls = ['https://www.theguardian.com/news/series/ten-best-photographs-of-the-day']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }
    rules = (
        Rule(LinkExtractor(
            restrict_xpaths=("//div[@class ='dcr-4z6ajs']//a[@data-link-name = 'media | group-0 | card-@1']")),
            callback='parse_item', follow=True),
            )

    def parse_item(self, response):
        caption_container = response.xpath("//div[@class='gallery__figcaption']")
        pictures_container = response.xpath("//div[@class='gallery__img-container gallery__img-container--landscape']")
        for items_caption, picture_item in zip(caption_container, pictures_container):
            custom_items = ApipicturesItem()  # Créer une nouvelle instance à chaque itération
            custom_items['media'] = response.xpath("//meta[@name='application-name']/@content").get()
            custom_items['sectionTitle'] = response.xpath("//title/text()").get().strip()
            caption_text = items_caption.xpath(
                "normalize-space(div[@class='gallery__caption']/text()[normalize-space()])").get()
            location = items_caption.xpath(".//h2/text()").get()
            author_item = items_caption.xpath(".//p[@class='gallery__credit']")
            author = author_item.xpath("substring-before(text(), '/')").get().replace('Photograph:', '').strip()
            credits_item = items_caption.xpath(".//p[@class='gallery__credit']")
            credits = credits_item.xpath("substring-after(text(), '/')").get().replace('Photograph:', '').strip()
            custom_items['caption'] = caption_text
            custom_items['location'] = location
            custom_items['author'] = author
            custom_items['credits'] = credits
            pubDate_raw = response.xpath("//meta[@property='article:published_time']/@content").get()
            custom_items['pubDate'] = datetime.strptime(pubDate_raw, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            custom_items['pageUrl'] = response.url
            picture_srcset = picture_item.xpath(".//picture/source/@srcset").get().replace('1000w', '')
            picture_urls = picture_srcset.split(", ")
            picture = picture_urls[0].split(" ")[0]
            custom_items['picture'] = picture
            custom_items['pictureEditor'] = response.xpath("//p[@class='byline']//a/span/text()").get()
            yield custom_items
