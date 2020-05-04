# -*- coding: utf-8 -*-
import scrapy

class ImageItem(scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_name = scrapy.Field()

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["culturadigital.udp.cl"]
    start_urls = ['http://culturadigital.udp.cl/index.php/coleccion/fondo-sills-y-gallardo/']

    '''
    def parse(self, response):
        #Get colections
        #iterate over colections
        #for colection_url in response.css("article.product_pod > h3 > a ::attr(href)").extract():
        colection_name = "fondo-sills-y-gallardo"
        colection_url = "http://culturadigital.udp.cl/index.php/coleccion/fondo-sills-y-gallardo"
        yield scrapy.Request(response.urljoin(colection_url), callback = self.parse_colection, meta={'colection': colection_name, 'colection_url': colection_url})
    '''
    
    #parse_colection
    def parse(self, response):
        colection = "fondo-sills-y-gallardo"
        colection_url = "http://culturadigital.udp.cl/index.php/coleccion/fondo-sills-y-gallardo"

        articles = response.css(".Elemento")
        #e = articles[7]
        for e in articles:
            links = e.css("a::attr(href)").extract()
            source = links[0]
            imgName = "".join(e.css("h2.Elemento__title").css("a::text").extract_first().split(" "))

            author = e.css(".Elemento__autor").css("a::text").extract_first()
            #TODO
            if author:
                author = "".join(author.split(" "))
            else:
                author = "NoTieneAutor"
            
            imgLink = e.css("img::attr(src)").extract_first()
            idSplit = imgLink.split("/")[-1].split(".")[0].split("-")
            imgId = "-".join([idSplit[0], idSplit[1]])
            finalImageName = "-".join([imgName, "por", author, colection, imgId])

            yield scrapy.Request(response.urljoin(colection_url), callback = self.download_img, meta={'imgLink': imgLink, 'finalImageName': finalImageName})
        #yield scrapy.Request(response.urljoin(colection), callback=self.download_img, meta={'imgLink': imgLink, 'finalImageName': finalImageName})
        '''
        item = ImageItem()
        img_urls = []
        img_urls.append(imgLink)
        item["image_urls"] = img_urls
        item["image_name"] = finalImageName
        return item
        '''
    
    def download_img(self, response):
        item = ImageItem()
        img_urls = []
        img_urls.append(response.meta.get('imgLink'))
        item["image_urls"] = img_urls
        item["image_name"] = response.meta.get('finalImageName')
        return item

    def parse_book_page(self, response):
        item = {}
        product = response.css("div.product_main")
        item["title"] = product.css("h1 ::text").extract_first()
        item['category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).extract_first()
        item['description'] = response.xpath(
            "//div[@id='product_description']/following-sibling::p/text()"
        ).extract_first()
        item['price'] = response.css('p.price_color ::text').extract_first()
        yield item


'''
next_page = response.css("li.next > a ::attr(href)").extract_first()
if next_page:
    yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
'''