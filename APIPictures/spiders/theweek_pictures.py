import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from APIPictures.items import ApipicturesItem


class TheweekPicturesSpider(CrawlSpider):
    name = "theweek_pictures"
    allowed_domains = ["theweek.com"]
    start_urls = ["https://theweek.com/photos"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//div[@class='polaris__article-card -layout-default -default polaris__article-group--single'][1]/a"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        container = response.xpath("//div[@class='polaris__single-slide--wrapper']")
        for item in container:
            custom_items = ApipicturesItem()
            custom_items['media'] = item.xpath("//meta[@property='og:site_name']/@content").get()
            custom_items['sectionTitle'] = response.xpath("//meta[@property='og:title']/@content").get()
            custom_items['pageUrl'] = response.url
            date_string = response.xpath("//span[contains(@class, 'polaris__date')]/text()").get()
            custom_items['pubDate'] = datetime.strptime(date_string, '%B %d, %Y' ).strftime('%Y-%m-%d')
            custom_items['caption'] = item.xpath("./div/div//p[1]/text()[1]").get()
            author_credits_item = item.xpath("./div/div//p[2]")
            custom_items['author'] = author_credits_item.xpath("substring-before(text(), '/')").get()
            custom_items['credits'] = author_credits_item.xpath("substring-after(text(), '/')").get()
            
            
            
            #custom_items['picture'] = item.xpath(".//figure/img/@data-src").get()
            img_srcset = item.xpath(".//figure/img/@data-srcset").get()
            
            image_links = img_srcset.split(',')
            
            full_desktop_link = None
            for link in image_links:
                if 'full-desktop' in link:
                    full_desktop_link = link.strip().split(' ')[0]
                    break
            custom_items['picture'] = 'https://mediacloud.theweek.com/image/upload/f_auto,' + full_desktop_link
            
            
            
            
            custom_items['location'] = 'Ref. to caption' 
            custom_items['pictureEditor'] = response.xpath("//div[@class='polaris__post-meta--author']/a/text()").get()
            yield custom_items
            


