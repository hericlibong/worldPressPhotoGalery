import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class CnnWeekPicsSpider(CrawlSpider):
    name = "cnn_week_pics"
    allowed_domains = ["edition.cnn.com"]
    start_urls = ["https://edition.cnn.com/world/photos"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//div[@class='container container_hero-card-feature world lazy']//a[1]"), callback="parse_item", follow=True),)


    def parse_item(self, response):
        container = response.xpath("//div[contains(@data-name, 'week in photos')]")
        for item in container:
            custom_items = ApipicturesItem()  # Créer une nouvelle instance à chaque itération
            custom_items['media'] = response.xpath("//meta[@property='og:site_name']/@content").get()
            custom_items['sectionTitle'] = response.xpath("//meta[@property = 'og:title']/@content").get()
            caption_element = item.xpath(".//div[@itemprop='caption']/span[@data-editable='metaCaption']")
            caption = item.xpath(".//span[@data-editable='metaCaption']/text()").get()
            normalized_caption = caption_element.xpath("normalize-space(.)").get()
            custom_items['caption'] = normalized_caption if normalized_caption else caption
            #publishedDdate_element = response.xpath("//p[@class='gallery-inline_unfurled__update-time']")
            #publishedDate_string= publishedDdate_element.xpath("substring-after(text(), '(2106 HKT)')").get().strip()
            custom_items['location'] = 'Ref. to caption'
            #custom_items['pubDate'] = datetime.strptime(publishedDate_string, '%B %d, %Y').strftime('%Y-%m-%d')
            custom_items['pubDate'] = response.xpath("substring(//meta[@property='article:published_time']/@content, 1, 10)").get()
            author_item = item.xpath(".//figcaption[@class='image__credit']")
            custom_items['author'] = author_item.xpath("substring-before(text(), '/')").get()
            custom_items['credits'] = author_item.xpath("substring-after(text(), '/')").get()
            custom_items['pageUrl'] = response.url 
            custom_items['picture'] = item.xpath(".//picture/img/@src").get() 
            custom_items['pictureEditor']= 'undefined'
            yield custom_items
