import scrapy
from scrapy.http import HtmlResponse
from ..items import Homework5Item


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/inzhener-pto.html']
    #['https://spb.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//a[@rel="next"]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        xpath = '//div[@class="f-test-search-result-item"]/div/div/div/div/div/div/div/div/div/div/div/span/a/@href'

        vacancies_links = response.xpath(xpath).getall()

        for link in vacancies_links:
            url = 'https://www.superjob.ru/'+link

            yield response.follow(url, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url

        slaray_xpath = '//span[@class="_2eYAG _3xCPT rygxv _3GtUQ"]//text()'
        vacancy_salary_raw = response.xpath(slaray_xpath).getall()
        vacancy_salary = self.parse_salary(vacancy_salary_raw)

        company_xpath = "//a[@class='_1IHWd f-test-link- YrERR']/@href"
        vacancy_company_name = response.xpath(company_xpath).get()

        yield Homework5Item(
            name=vacancy_name,
            url=vacancy_url,
            salary_min=vacancy_salary['min'],
            salary_max=vacancy_salary['max'],
            salary_currency=vacancy_salary['currency'],
            salary_tax=vacancy_salary['tax'],
            salary_raw=vacancy_salary_raw,
            company_name=vacancy_company_name,
            company_name_raw=None
        )

    def parse_salary(self, salary_data: list) -> dict:

        salary = {
            'min': None,
            'max': None,
            'currency': None,
            'tax': None
        }

        if len(salary_data) == 3:
            if salary_data[0] == 'до':
                value_list = salary_data[2].split(u'\xa0')
                salary['max'] = int(value_list[0]+value_list[1])
                salary['currency'] = value_list[2]

            elif salary_data[0] == 'от':
                value_list = salary_data[2].split(u'\xa0')
                salary['min'] = int(value_list[0]+value_list[1])
                salary['currency'] = value_list[2]

        elif len(salary_data) == 7:
            salary['min'] = int(salary_data[0].replace(u'\xa0', ''))
            salary['max'] = int(salary_data[4].replace(u'\xa0', ''))
            salary['currency'] = salary_data[6]

        return salary
