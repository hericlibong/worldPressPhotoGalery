# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from datetime import datetime
# from APIPictures.items import ApipicturesItem


# class WeltPicSpider(CrawlSpider):
#     name = 'welt_pic'
#     allowed_domains = ['welt.de']
#     start_urls = ['https://www.welt.de/vermischtes/bilder-des-tages/']

#     rules = (
#         Rule(LinkExtractor(restrict_xpaths="//div[@class='u-grid-container c-stage__teasers']/div[1]//a[1]"), callback='parse_item', follow=True),
#     )

#     def parse_item(self, response):
#         container = response.xpath("//figure[@class='o-element__main o-element__main--is-colored']")
#         for item in container:
#             custom_items = ApipicturesItem()
#             custom_items['media'] = response.xpath("//meta[@property='og:site_name']/@content").get()
#             custom_items['sectionTitle'] = response.xpath("//meta[@property='og:title']/@content").get()
#             custom_items['pageUrl'] = response.url
#             custom_items['pubDate'] = response.xpath("//meta[@name='date']/@content").get()
#             author_credit_items = item.xpath(".//figcaption//p[@class='o-element__text o-element__text--is-small']/text()").get().replace('Quelle:', '')
#             custom_items['credits'], custom_items['author'] = author_credit_items.split('/')[0].strip(), author_credit_items.split('/')[1].strip()
#             custom_items['picture'] = item.xpath(".//picture[@class='o-element__image c-gallery-image-element__image']//img/@data-src").get()
#             custom_items['location'] = 'Ref. to caption'
#             custom_items['pictureEditor'] = 'Unspecified'
#             yield custom_items
