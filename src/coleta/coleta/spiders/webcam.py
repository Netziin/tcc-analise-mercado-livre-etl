import scrapy


class WebcamSpider(scrapy.Spider):
    name = "webcam"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/webcam#D[A:webcam]"]
    def parse(self, response):

        products = response.css('div.ui-search-result__wrapper') 

        for product in products:

            prices= product.css('span.andes-money-amount__fraction::text').getall()

            review_block = product.css('span.poly-component__review-compacted')

            labels = review_block.css('span.poly-phrase-label::text').getall()

            rating = labels[0] if len(labels) > 0 else None
            sales = labels[1] if len(labels) > 1 else None

            yield {
            'category': 'Webcam', 
            'brand': product.css('span.poly-component__brand::text').get(),
            'name': product.css('a.poly-component__title::text').get(),
            'seller': product.css('span.poly-component__seller::text').get(),
            'reviews_rating_number': rating,
            'reviews_amount': sales,
            'new_money': prices[0] if len (prices) > 0 else None,
            'old_money': prices[1] if len (prices) > 1 else None
        }