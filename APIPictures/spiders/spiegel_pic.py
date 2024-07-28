# import scrapy
# from datetime import datetime
# from APIPictures.items import ApipicturesItem


# class SpiegelPicSpider(scrapy.Spider):
#     name = 'spiegel_pic'
#     allowed_domains = ['spiegel.de']
#     start_urls = ['https://www.spiegel.de/fotostrecke/bilder-des-tages-fotos-aus-deutschland-und-der-welt-fotostrecke-122824.html']

#     def parse(self, response):
#         custom_items = ApipicturesItem()
#         custom_items['media'] = response.xpath("//meta[@name='author']/@content").get()
#         custom_items['sectionTitle'] = response.xpath("//span[@class='align-middle'][1]/text()").get()
#         custom_items['pageUrl'] = response.url
#         custom_items['pubDate'] = response.xpath("//meta[@name='date']/@content").get()
#         custom_items['caption'] = response.xpath("//figure[1]/figcaption//p[2]/text()").get()
#         auteur_credit_text = response.xpath("//figure[1]/figcaption/div[contains(@class, 'RichTextCredit')]/text()").get().replace('Foto:', '')
#         custom_items['author'], custom_items['credits'] = auteur_credit_text.split('/')[0].strip(), auteur_credit_text.split('/')[1].strip()
#         picture_item = response.xpath("//figure[1]//picture/source/@data-srcset").get()
#         custom_items['picture'] = picture_item.split(',')[0].split()[0]
#         custom_items['location'] = 'Ref. to caption'
#         custom_items['pictureEditor'] = 'Unspecified'
#         yield custom_items
