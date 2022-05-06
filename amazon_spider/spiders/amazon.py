import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = [
        'https://www.amazon.co.uk/kindle-dbs/entity/author/B09L6K18C3?_encoding=UTF8&page=2'
    ]

    def parse(self, response):
        products = response.xpath('*//div[contains(@class,"s-result-item")]')

        for product in products:
            name = product.css('h2 span::text').get()
            link = 'https://www.amazon.com' +  product.css('h2 a::attr(href)').get() if product.css('h2 a::attr(href)').get() else None

            if link:
                yield scrapy.Request(
                    url = link,
                    callback = self.parse_details,
                    meta = {
                        'link': link
                    }
                )

        next_page = response.xpath('*//ul[@class="a-pagination"]//li[@class="a-last"]//a/@href').extract_first()
        if next_page:    
            print(f'Going for next page! {next_page}')            
            yield response.follow(
                url = next_page,
                callback = self.parse
            )
    
    def parse_details(self, response):
        name = response.xpath('*//span[@id="productTitle"]/text()').extract_first()
        rating = response.css('i.a-icon.a-icon-star span.a-icon-alt::text').get()
        cover_image = response.css('img#imgBlkFront::attr(src)').get()
        price = response.css('span#price::text').get()
        variations = response.css('div#tmmSwatches ul li a.a-button-text span:nth-child(1)::text').getall()
        bsr = response.xpath('*//span[contains(text(),"Best Sellers Rank")]/parent::span/text()[2]').extract_first()
        yield {
            'name': name.strip() if name else None,
            'link': response.meta['link'],
            'rating': rating,
            'cover_image': cover_image,
            'price': price,
            'variations': variations,
            'bsr': bsr
        }
