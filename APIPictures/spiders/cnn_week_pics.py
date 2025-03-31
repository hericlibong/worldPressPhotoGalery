from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class CnnWeekPicsSpider(CrawlSpider):
    name = "cnn_week_pics"
    allowed_domains = ["edition.cnn.com"]
    start_urls = ["https://edition.cnn.com/world/photos"]
    rules = (Rule(LinkExtractor(restrict_xpaths="//a[contains(., 'The week in ')]"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        container = response.xpath("//div[@data-component-name='image']")
        for item in container:
            custom_items = ApipicturesItem()
            # Extraire le nom du média
            custom_items['media'] = response.xpath("//meta[@property='og:site_name']/@content").get()
            # Extraire le titre de la section
            custom_items['sectionTitle'] = response.xpath("//meta[@property='og:title']/@content").get()
            # Extraire la légende de l'image
            caption_element = item.xpath(".//div[@itemprop='caption']/span[@data-editable='metaCaption']")
            caption = caption_element.xpath("normalize-space(.)").get()
            custom_items['caption'] = caption
            # Référence à la légende pour localisation
            custom_items['location'] = 'Ref. to caption'
            # Extraire la date de publication
            pubdate_raw = response.xpath("//meta[@property='article:published_time']/@content").get()
            custom_items['pubDate'] = datetime.strptime(pubdate_raw, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            # Extraire l'auteur de l'image
            author_item = item.xpath(".//figcaption[@class='image__credit']")
            custom_items['author'] = author_item.xpath("substring-before(text(), '/')").get()
            # Extraire les crédits de l'image
            custom_items['credits'] = author_item.xpath("substring-after(text(), '/')").get()
            # Extraire l'URL de la page
            custom_items['pageUrl'] = response.url
            # Extraire l'URL de l'image
            custom_items['picture'] = item.xpath(".//picture/source/@srcset[1]").get()
            # Définir l'éditeur de l'image
            custom_items['pictureEditor'] = 'undefined'
            yield custom_items
