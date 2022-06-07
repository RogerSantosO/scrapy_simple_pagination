import scrapy


class TdealSpider(scrapy.Spider):
    name = 'tdeal'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html']

    def parse(self, response):
        produtos = response.xpath('//div[@class="r_b_c"]/ul/div/li')
        for produto in produtos:
            yield {
            'name':produto.xpath('.//a[2][@class="p_box_title"]/text()').get(),
            'original price':produto.xpath('.//div[2]/span[@class="normalprice fl"]/text()').get(),
            'discounted price':produto.xpath('.//div[2]/span[@class="productSpecialPrice fl"]/text()').get(),
            'url': response.urljoin(produto.xpath('.//a/@href').get())
                }
            
        next_page = response.xpath('//a[@class="nextPage"]/@href').get()
        
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)