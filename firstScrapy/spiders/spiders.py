import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from firstScrapy.items import FirstscrapyItem
from scrapy.exceptions import CloseSpider

class FirstscrapySpider(CrawlSpider):
	name = 'firstScrapy'
	item_count = 0
	allowed_domain = ['https://www.mundounico.com.co/']
	start_urls = ['https://www.mundounico.com.co/colors/']

	rules = {
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//h3[@class="item__showcase__title"]')),
			callback = 'parse_item', follow=False)
	}

	def parse_item(self, response):
		mu_item = FirstscrapyItem()
		mu_item['titulo'] = response.xpath('normalize-space(//div[contains(@class, "productName")and contains(@class, "fn")]/text())').extract()
		mu_item['precio'] = response.xpath('//strong[(@class="skuBestPrice")]/text()').extract()
		mu_item['tallas'] = response.xpath('normalize-space(//div[(@class="edd-group")]/text())').extract()
		mu_item['descripcion'] = response.xpath('//div[(@class="productDescription")]/text()').extract()
		self.item_count += 1
		if self.item_count > 15:
			raise CloseSpider('item_exceeded')
		yield mu_item