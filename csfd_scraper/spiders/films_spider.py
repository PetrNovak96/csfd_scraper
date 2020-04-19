import scrapy

from csfd_scraper.items import FilmItem


class FilmsSpider(scrapy.Spider):

    name = "films"

    def start_requests(self):
        urls = [
            'https://www.csfd.cz/zebricky/nejlepsi-filmy/',
            'https://www.csfd.cz/zebricky/nejhorsi-filmy/',
            'https://www.csfd.cz/zebricky/nejoblibenejsi-filmy/',
            'https://www.csfd.cz/zebricky/nejrozporuplnejsi-filmy/',
            'https://www.csfd.cz/zebricky/nejoblibenejsi-filmy/',

        ]

        search_url = 'https://www.csfd.cz/podrobne-vyhledavani/?type%5B%5D=0&type%5B%5D=2&type%5B%5D=3&type%5B%5D=4&type%5B%5D=5&type%5B%5D=6&type%5B%5D=7&type%5B%5D=8&type%5B%5D=9&type%5B%5D=14&genre%5Btype%5D=2&genre%5Binclude%5D%5B%5D=&genre%5Bexclude%5D%5B%5D=&origin%5Btype%5D=2&origin%5Binclude%5D%5B%5D=&origin%5Bexclude%5D%5B%5D=&year_from=&year_to=&rating_from=&rating_to=&actor=&director=&composer=&screenwriter=&author=&cinematographer=&production=&edit=&sound=&scenography=&mask=&costumes=&tag=&ok=Hledat&_form_=film'
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse_chart)

        yield scrapy.Request(url=search_url,callback=self.parse_search)

    def parse_chart(self,response):
        yield from response.follow_all(css='td.film a', callback=self.parse_record)

    def parse_record(self, response):
        record_type = response.css('div.info div.header h1 span.film-type::text').get()
        record_type = 'film' if record_type is None else record_type[1:-1]
        record_link_text = response.css('div.info div.header h1 a::text').get('').strip()
        if len(record_link_text) > 0:
            following = response.xpath('//div[@class="info"]/div[@class="header"]/h1/a/following-sibling::node()').get()
            name = record_link_text + following
            name = name.strip()
        else:
            name = response.css('div.info div.header h1::text').get().strip()
        country = response.css('div.info p.origin::text').get()
        country = country.split(',')[0] if country is not None else ''
        year = response.css('div.info p.origin span::text').re(r'(\d{4})')
        year = year[0] if len(year) > 0 else ''
        genre = response.css('div.info p.genre::text').get()
        rating = response.css('#rating h2.average::text').re(r'(\d+)')
        rating = rating[0] if len(rating) > 0 else ''
        duration = response.css('div.info p.origin::text').re(r'(\d+)')
        duration = duration[0] if len(duration) > 0 else ''
        comments_count = response.css('div.ct-general div.header h2 a::text')
        comments_count = comments_count[1].re(r'(\d+)')[0] \
            if len(comments_count) > 1 and len(comments_count[1].re(r'(\d+)')) > 0 \
            else 0
        url = response.url
        yield FilmItem(
            name=name,
            country=country,
            rating=rating,
            duration=duration,
            year=year,
            comments_count=comments_count,
            genre=genre,
            record_type=record_type,
            url=url,
        )
        yield from response.follow_all(css='div.similar li a', callback=self.parse_record)
        yield from response.follow_all(css='div.tags a', callback=self.parse_search)

    def parse_search(self,response):
        yield from response.follow_all(css='td.name a', callback=self.parse_record)
        yield from response.follow_all(css='#films div.paginator a', callback=self.parse_search)

