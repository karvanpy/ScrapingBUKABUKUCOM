import scrapy

class BukaBukuCom(scrapy.Spider):
	name = 'bukabukucom'
	start_urls = ['http://www.bukabuku.com/browses/index/dept:book/cid:253/komputer.html/']

	def parse(self, response):
		books = response.css('div.product_list_grid')
		
		for book in books:
			# book_title = book.css('span.product_list_title > a::text').get()
			book_url = 'http://www.bukabuku.com' + book.css('span.product_list_title > a').attrib['href']
			# book_author = book.css('div.product_author.text_smaller::text').get().strip().replace('\t', '').replace('oleh', '')
			# book_price = book.css('span.price::text').get()
			# book_url_details = scrapy.Request(url=book_url, callback=self.parse_details)
			yield scrapy.Request(url=book_url, callback=self.parse_details)

			# yield {
			# 	'book_title' : book_title,
			# 	'book_url' : book_url,
			# 	'book_author' : book_author,
			# 	'book_price' : 'Stock tidak tersedia' if book_price is None else book_price.strip().replace('\t', ''),
			# 	'book_url_details' : dir(book_url_details)
			# 	}

		next_page = response.css('div.next > a::attr(href)').get()
		if next_page:
			yield response.follow(next_page, callback=self.parse)

	def parse_details(self, response):
		product_details_title = response.xpath('//div[@class="product_detail"]/table[3]/tr/td[1]/text()').getall()
		product_details_desc  = response.xpath('//div[@class="product_detail"]/table[3]/tr/td[3]/text()').getall()

		product_details_title = list(map(lambda x: x.lower().replace(' ', '_'), product_details_title))
		product_details_desc  = list(map(lambda x: x.strip(), product_details_desc))

		product_details 	  = dict(zip(product_details_title, product_details_desc))
		if 'penerbit' in product_details.keys():
			product_details.update({
				'penerbit' : response.xpath('//div[@class="product_detail"]/table[3]/tr/td[3]/a/text()').get()
					})
		
		book_title    		= response.css('span.product_title::text').get().strip()
		book_description	= response.css('div.product_description > pre > span::text').get()
		book_author   		= response.css('span.product_author > a.blue_link::text').get()
		book_price    		= response.css('span.price::text').get()

		book_isbn13   		= product_details.get('isbn13') #[-4] if 'ISBN13' in product_details else None
		book_tanggal_terbit = product_details.get('tanggal_terbit')
		book_bahasa   		= product_details.get('bahasa')
		book_penerbit 		= product_details.get('penerbit') # response.xpath('//div[@class="product_detail"]/table[3]/tr/td[3]/a/text()').get()

		book_details 		= {
			'book_title' 	  	: book_title,
			'book_description'	: book_description,
			'book_author' 	 	: book_author,
			'book_price' 	 	: 'Stock tidak tersedia' if book_price is None else book_price.strip().replace('\t', ''),
			'isbn13' 		 	: book_isbn13,
			'tanggal_terbit' 	: book_tanggal_terbit,
			'bahasa' 		 	: book_bahasa,
			'penerbit' 		 	: book_penerbit,
			'url' 			 	: response.url
		}

		yield book_details