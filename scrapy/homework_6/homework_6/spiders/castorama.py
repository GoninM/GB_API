import scrapy
from scrapy.http import HtmlResponse
from homework_6.items import Homework6Item
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/catalogue/']

    def parse(self, response: HtmlResponse):
        xpath = "//a[@class ='category__link']"

        category_url = response.xpath(xpath)
        if category_url:
            for category in category_url:
                yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response: HtmlResponse):
        xpath = "//a[@class='category__link sitemap-level-1-link'] | " \
                "//a[@class ='grandchild__link sitemap-level-2-link']"

        subcategory_url = response.xpath(xpath)

        if subcategory_url:
            for subcategory in subcategory_url:
                yield response.follow(subcategory, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse_product)

        xpath = "//a[@class ='product-card__img-link']"

        product_url = response.xpath(xpath)
        if product_url:
            for product in product_url:
                yield response.follow(product, callback=self.parse_data)

    def parse_data(self, response: HtmlResponse):
        loader = ItemLoader(item=Homework6Item(), response=response)
        loader.add_xpath('name', "//h1//text()")
        loader.add_xpath('price', "//div[@class='price-box']/span/span/span/span//text()")
        loader.add_xpath('price_raw', "//div[@class='price-box']/span/span/span/span//text()")

        xpath_photo = "//ul[@class='swiper-wrapper']/li/img/@data-src | " \
                      "//ul[@class='swiper-wrapper']/li/div/img/@data-src"

        # xpath_photo = "//ul[@class='swiper-wrapper']/li/div/img/@data-src"
        loader.add_xpath('photos', xpath_photo)

        loader.add_value('url', response.url)

        xpath_params = "//div[@class='product-block product-specifications']/dl/dt/span//text() | " \
                       "//div[@class='product-block product-specifications']/dl/dd//text()"
        loader.add_xpath('params', xpath_params)

        yield loader.load_item()





