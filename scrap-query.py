from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

process = CrawlerProcess(get_project_settings())

process.crawl('query')
process.start() # the script will block here until the crawling is finished
