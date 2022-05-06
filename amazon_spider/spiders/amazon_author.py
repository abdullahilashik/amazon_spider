import scrapy


class AmazonAuthorSpider(scrapy.Spider):
    name = 'amazon-author'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.co.uk/kindle-dbs/entity/author/B09L6K18C3?_encoding=UTF8&page=2']

    def start_requests(self):
        for i in range(10):
            yield scrapy.Request(
                url=f'https://www.amazon.co.uk/kindle-dbs/entity/author/B09L6K18C3?_encoding=UTF8&page={i}',
                callback=self.parse
            )

    def parse(self, response):
        items = response.css('div.a-fixed-left-grid.a-spacing-medium')
        for item in items:
            name = item.css('a.a-link-normal span::text').get()
            author = item.css('a.a-size-base.a-link-normal span::text').get()
            price = item.css('span.a-color-price::text').get()
            book_type_paperback = item.css('a[aria-label^="Paperback"] span::text').get()
            book_type_hardcover = item.css('a[aria-label^="Hardcover"] span::text').get()
            stars = item.css('i.authorBookReviewStars::attr(class)').get()
            link = item.css('a.a-link-normal::attr(href)').get()

            meta = {
                'name': name.strip(),
                'author': author.strip() if author else '',
                'price': price.strip() if price else '',
                'book_type': book_type_paperback,
                'book_type_hardcover': book_type_hardcover,
                'stars': stars.replace('a-icon a-icon-star a-star-', '').replace(' authorBookReviewStars',
                                                                                 '') if stars else 0,
            }

            yield response.follow(
                url=link,
                callback=self.parse_details,
                meta=meta
            )

    def parse_details(self, response):
        name = response.meta['name']
        author = response.meta['author']
        price = response.meta['price']
        book_type = response.meta['book_type']
        book_type_hardcover = response.meta['book_type_hardcover']
        stars = response.meta['stars'].replace('-', '.')
        bsr = response.xpath('*//span[contains(text(),"Best Sellers Rank")]/parent::span/text()[2]').extract_first()
        cover_image = response.css('img#imgBlkFront::attr(src)').get()

        yield {
            'name': name,
            'author': author,
            'price': price,
            'book_type': book_type,
            'book_type_hardcover': book_type_hardcover,
            'stars': stars,
            'bsr': bsr,
            'cover_image': cover_image
        }
