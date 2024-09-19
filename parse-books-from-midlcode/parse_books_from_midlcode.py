import scrapy
import wget
import re


class ParseBooksFromMidlcodeSpider(scrapy.Spider):
    name = "parse_books_from_midlcode"
    allowed_domains = ["midlcode.com"]
    start_urls = ["https://midlcode.com/ru/books/"]

    def parse(self, response):
        books_urls = response.css('div.cart3 a::attr(href)').getall()
        for book_url in books_urls:
            yield scrapy.Request(url=f'https://midlcode.com{book_url}', callback=self.parse_detail)

    def parse_detail(self, response):
        for pdf_url in response.xpath("//*[@id='downloadAgain']/a/@href").extract():
            book_name = response.css('h1.text-centr::text').get()

            book_name = book_name.replace('.', ' ').replace(',', ' ')
            book_name = re.sub(r'\s+', ' ', book_name)
            book_name = book_name.replace(' ', '_')

            if book_name[0] == '_':
                book_name = book_name[1:]
            if book_name[-1] == '_':
                book_name = book_name[:-1]

            wget.download(
                f'https://midlcode.com{pdf_url}',
                out=f'/home/alice/ShitCode/mini-scripts/parse-books-from-midlcode/books/{book_name}.pdf'
            )

