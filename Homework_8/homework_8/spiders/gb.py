import scrapy
from scrapy import FormRequest, Request
from scrapy.http import HtmlResponse
import requests
from homework_8.items import Homework8Item
from homework_8.params import USER_EMAIL, USER_PASSWORD


class GbSpider(scrapy.Spider):
    name = 'gb'
    allowed_domains = ['gb.ru']
    start_urls = ['https://gb.ru/login']

    def parse(self, response: HtmlResponse):
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').get()

        yield FormRequest.from_response(response,
                                        formxpath='//form[@id="new_user"]',
                                        formdata={
                                            'authenticity_token': authenticity_token,
                                            'user[email]': USER_EMAIL,
                                            'user[password]': USER_PASSWORD,
                                            'user[remember_me]': '0',

                                        },
                                        callback=self.after_login
                                        )

    def after_login(self, response: HtmlResponse):
        if response.xpath("//div[@class='mn-btn-icon']"):
            yield response.follow('https://gb.ru/career', callback=self.parse_carreer)

    def parse_carreer(self, response: HtmlResponse):
        next_page_url = response.xpath('//a[@rel="next"]/@href').get()

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_carreer)

        vacansies_urls = response.xpath('//div[@class="project project_company "]/a/@href').getall()

        if vacansies_urls:
            for vacansies_url in vacansies_urls:
                url = 'https://gb.ru' + vacansies_url
                yield response.follow(url, callback=self.parse_vacancies)

    def parse_vacancies(self, response: HtmlResponse):
        vac_number = response.url.split('/')[-1]

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}

        company_info = requests.get(url=f'https://gb.ru/api/v2/projects/{vac_number}',
                                    headers=headers).json()

        company_vacancies = requests.get(url=f'https://gb.ru/api/v2/projects/{vac_number}/vacancies',
                                         headers=headers).json()

        for vacancy in company_vacancies:
            yield Homework8Item(
                vacancy_name=vacancy['vacancy']['title'],
                vacancy_description=vacancy['vacancy']['description'],
                vacancy_salary_amount=vacancy['vacancy']['salary_amount'],
                vacancy_positions_count=vacancy['vacancy']['positions_count'],
                vacancy_salary_period=vacancy['vacancy']['salary_period'],
                vacancy_state=vacancy['vacancy']['state'],
                vacancy_positions_last=vacancy['vacancy']['positions_last'],
                vacancy_test_job=vacancy['vacancy']['test_job'],
                vacancy_city=vacancy['vacancy']['city'],
                vacancy_salary_min=vacancy['vacancy']['salary_min'],
                vacancy_salary_max=vacancy['vacancy']['salary_max'],
                company_name=company_info['project']['title'],
                company_contract_signed=company_info['project']['contract_signed'],
                company_name_description=company_info['project']['html'],
            )
