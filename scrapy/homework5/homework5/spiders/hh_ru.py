import scrapy
from scrapy.http import HtmlResponse
from ..items import Homework5Item

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'

    allowed_domains = ['hh.ru']

    start_urls = \
        ['https://spb.hh.ru/search/vacancy?text=juniorpython&salary=&area=1&ored_clusters=true&enable_snippets=true&items_on_page=20'] #,
         # 'https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=junior+python&ored_clusters=true&enable_snippets=true']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath('//a[@data-qa="serp-item__title"]/@href').getall()

        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_salary(self, salary_data: list) -> dict:

        salary = {
            'min': None,
            'max': None,
            'currency': None,
            'tax': None
        }

        if len(salary_data) == 6:
            if salary_data[0] == 'до ':
                salary['max'] = int(salary_data[1].replace(u'\xa0', ''))

            elif salary_data[0] == 'от ':
                salary['min'] = int(salary_data[1].replace(u'\xa0', ''))

            salary['currency'] = salary_data[3]
            salary['tax'] = salary_data[5]

        elif len(salary_data) == 8:
            salary['min'] = int(salary_data[1].replace(u'\xa0', ''))
            salary['max'] = int(salary_data[3].replace(u'\xa0', ''))
            salary['currency'] = salary_data[5]
            salary['tax'] = salary_data[7]

        return salary

    def convert_company_name_from_list_to_str(self, raw_data: list) -> str:
        result = ''

        if len(raw_data) == 2:
            result += raw_data[0].replace(u'\xa0', '')

        elif len(raw_data) == 4:
            result += raw_data[0].replace(u'\xa0', '')
            result += ' '
            result += raw_data[1].replace(u'\xa0', '')

        else:
            pass

        return result

    def parse_vacancy(self, response: HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url

        vacancy_salary_raw = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()
        vacancy_salary = self.parse_salary(vacancy_salary_raw)

        vacancy_company_name_raw = response.xpath('//a[@data-qa="vacancy-company-name"]//text()').getall()
        vacancy_company_name = self.convert_company_name_from_list_to_str(vacancy_company_name_raw)

        yield Homework5Item(
            name=vacancy_name,
            url=vacancy_url,
            salary_min=vacancy_salary['min'],
            salary_max=vacancy_salary['max'],
            salary_currency=vacancy_salary['currency'],
            salary_tax=vacancy_salary['tax'],
            salary_raw=vacancy_salary_raw,
            company_name=vacancy_company_name,
            company_name_raw=vacancy_company_name_raw
        )



