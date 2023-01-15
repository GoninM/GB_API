from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
# from  scrapy.utils.reactor import install_reactor

from spiders.hh_ru import HhRuSpider
from spiders.superjob_ru import SuperjobRuSpider


if __name__ == '__main__':
    configure_logging()

    settings = get_project_settings()

    runner = CrawlerRunner(settings)
    runner.crawl(HhRuSpider)
    runner.crawl(SuperjobRuSpider)

    reactor.run()
