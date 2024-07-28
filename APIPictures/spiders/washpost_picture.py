# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from datetime import datetime
# from APIPictures.items import ApipicturesItem


# class WashpostPictureSpider(CrawlSpider):
#     name = "washpost_picture"
#     allowed_domains = ["washingtonpost.com"]
#     start_urls = ["https://www.washingtonpost.com/photography"]

#     rules = (Rule(LinkExtractor(restrict_xpaths="//div[@class='story-body col-lg-12 col-md-12']/div/h2/a"), callback="parse_item", follow=True),)

#     def start_requests(self):
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
#         }
#         for url in self.start_urls:
#             yield scrapy.Request(url, headers=headers)

#     def parse_item(self, response):
#         container = response.xpath("//amp-story-page[contains(@id, 'slide')]")
#         for item in container[1:]:
#             custom_items = ApipicturesItem()
#             custom_items['media'] = response.xpath("//meta[@property='og:site_name']/@content").get()
#             custom_items['caption'] = item.xpath(".//amp-story-grid-layer/div[@class='caption-container']/p[2]/text()").get()
#             custom_items['picture'] = item.xpath(".//amp-img/@src").get()
#             location_date_element = item.xpath(".//amp-story-grid-layer/div[@class='caption-container']/p[1]")
#             custom_items['location'] = location_date_element.xpath("substring-after(text(), '|')").get()
#             credit_author_element = item.xpath(".//amp-story-grid-layer/div[@class='caption-container']/p[contains(@class, 'credit')]")
#             custom_items['author'] = credit_author_element.xpath("substring-before(text(), '/')").get()
#             custom_items['credits'] = credit_author_element.xpath("substring-after(text(), '/')").get()
#             custom_items['pageUrl'] = response.url
#             custom_items['sectionTitle'] = response.xpath("//meta[@property='og:title']/@content").get()
#             #pub_date_string = response.xpath("//amp-story-grid-layer/div[@class='pg-headline text-center']//span/text()").get().replace('|', '').strip()
#             pub_date_string = response.xpath("//span[contains(@class, 'date')]/text()").get().replace('|', '').strip()
#             custom_items['pubDate'] = datetime.strptime(pub_date_string, '%b %d, %Y').strftime('%Y-%m-%d')
#             custom_items['pictureEditor'] = response.xpath("substring-after(//p[@class='byline']/text(), 'By')").get().strip()

#             yield custom_items

#             #//amp-story-page[contains(@id, 'slide')]//amp-story-grid-layer/div[@class='caption-container']/p[contains(@class, 'credit')]
