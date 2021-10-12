import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = [
        'https://www.amazon.com/s?i=stripbooks&rh=p_27%3ASweet+Harmony+Press&s=relevancerank&text=Sweet+Harmony+Press&ref=dp_byline_sr_pop_book_1',
        'https://www.amazon.com/s?i=stripbooks&rh=p_27%3ADream%27s+Art&s=relevancerank&text=Dream%27s+Art&ref=dp_byline_sr_book_1',
        'https://www.amazon.com/s?i=stripbooks&rh=p_27%3ACreative+Gifts+Studio&s=relevancerank&text=Creative+Gifts+Studio&ref=dp_byline_sr_book_1',
        'https://www.amazon.com/s?i=stripbooks&rh=p_27%3AActive+Mind&s=relevancerank&text=Active+Mind&ref=dp_byline_sr_book_1',
        'https://www.amazon.com/s?i=stripbooks&rh=p_27%3ATeam+Notebook+Usa+Notebook+team&s=relevancerank&text=Team+Notebook+Usa+Notebook+team&ref=dp_byline_sr_book_1',        
        'https://www.amazon.com/s/ref=dp_byline_sr_book_1?ie=UTF8&field-author=outzy+publishing&text=outzy+publishing&sort=relevancerank&search-alias=books'
        'https://www.amazon.com/s/ref=dp_byline_sr_book_1?ie=UTF8&field-author=BOHEMIAN+FLAVOR&text=BOHEMIAN+FLAVOR&sort=relevancerank&search-alias=books',
        'https://www.amazon.com/s/ref=dp_byline_sr_book_1?ie=UTF8&field-author=Bujo+Heaven&text=Bujo+Heaven&sort=relevancerank&search-alias=books',
        'https://www.amazon.com/s/ref=dp_byline_sr_book_1?ie=UTF8&field-author=Creative+PositivePress&text=Creative+PositivePress&sort=relevancerank&search-alias=books',
        'https://www.amazon.com/s/ref=dp_byline_sr_book_1?ie=UTF8&field-author=Employees+Quotes&text=Employees+Quotes&sort=relevancerank&search-alias=books',
        'https://www.amazon.com/s/ref=dp_byline_sr_book_1?ie=UTF8&field-author=Employeehmz&text=Employeehmz&sort=relevancerank&search-alias=books',
        'https://www.amazon.com/s/ref=dp_byline_sr_book_1?ie=UTF8&field-author=GIFT+NOTEBOOK&text=GIFT+NOTEBOOK&sort=relevancerank&search-alias=books'
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

        yield {
            'name': name,
            'link': response.meta['link'],
            'rating': rating,
            'cover_image': cover_image
        }
