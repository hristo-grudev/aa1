import scrapy

from scrapy.loader import ItemLoader
from ..items import Aa1Item
from itemloaders.processors import TakeFirst


class Aa1Spider(scrapy.Spider):
	name = 'aa1'
	start_urls = ['https://www.aa1.de/presse/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="block-accordion__text"]/ul/li')
		for post in post_links:
			url = post.xpath('.//a/@href').get()
			date = post.xpath('.//span/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1//text()|//h2//text()').get()
		description = response.xpath('//article/p//text()|//article//li//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=Aa1Item(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
