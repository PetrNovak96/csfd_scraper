import scrapy

from csfd_scraper.items import FilmItem, ParticipationItem, ParticipantItem


class FilmsSpider(scrapy.Spider):

    name = "films"
    main_url = "https://www.csfd.cz"

    def start_requests(self):
        urls = [
            self.main_url + '/zebricky/nejlepsi-filmy/?show=complete',
            self.main_url + '/zebricky/nejhorsi-filmy/?show=complete',
            self.main_url + '/zebricky/nejoblibenejsi-filmy/?show=complete',
            self.main_url + '/zebricky/nejrozporuplnejsi-filmy/?show=complete',
            self.main_url + '/zebricky/nejoblibenejsi-filmy/?show=complete',
            self.main_url + '/zebricky/nejlepsi-serialy/?show=complete',
            self.main_url + '/zebricky/nejhorsi-serialy/?show=complete',
            self.main_url + '/zebricky/nejoblibenejsi-serialy/?show=complete',
        ]

        search_url = self.main_url + '/podrobne-vyhledavani/?type%5B%5D=0&type%5B%5D=2&type%5B%5D=3&type%5B%5D=4&type%5B%5D=5&type%5B%5D=6&type%5B%5D=7&type%5B%5D=8&type%5B%5D=9&type%5B%5D=14&genre%5Btype%5D=2&genre%5Binclude%5D%5B%5D=&genre%5Bexclude%5D%5B%5D=&origin%5Btype%5D=2&origin%5Binclude%5D%5B%5D=&origin%5Bexclude%5D%5B%5D=&year_from=&year_to=&rating_from=&rating_to=&actor=&director=&composer=&screenwriter=&author=&cinematographer=&production=&edit=&sound=&scenography=&mask=&costumes=&tag=&ok=Hledat&_form_=film'

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse_chart)

        yield scrapy.Request(url=search_url,callback=self.parse_search)

    def parse_chart(self,response):
        yield from response.follow_all(css='td.film a', callback=self.parse_record)

    def parse_record(self, response):
        record_item = self.map_film_item(response)
        record_url = record_item['url']
        yield record_item

        participation_xpath = '//div[@class="creators"]/div[h4 = "%s:"]/span/a/@href'
        participation_types = {
            'actor': "Hrají",
            'director': "Režie",
            'writer': "Předloha",
            'scenario': "Scénář",
            'music': "Hudba",
            'camera': "Kamera",
        }
        for participation_type in participation_types.items():
            url_paths = response.xpath(participation_xpath % participation_type[1])
            for url_path in url_paths:
                participant_url = url_path.get()
                yield ParticipationItem(
                    film_url=record_url,
                    participant_url= self.main_url + participant_url,
                    type=participation_type[0]
                )
                yield response.follow(participant_url, callback=self.map_participant_item)

        yield from response.follow_all(css='div.similar li a', callback=self.parse_record)
        yield from response.follow_all(css='div.tags a', callback=self.parse_search)

    def parse_search(self,response):
        yield from response.follow_all(css='td.name a', callback=self.parse_record)
        yield from response.follow_all(css='#films div.paginator a', callback=self.parse_search)

    @staticmethod
    def map_film_item(response):
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
        return FilmItem(
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

    @staticmethod
    def map_participant_item(response):
        url = response.url
        name = response.css(".info h1::text").get('').strip()
        photo = response.css(".creator-photo").xpath("@src").re(r'(.+)(?=\?)')
        photo = 'https:' + photo[0] if len(photo) > 0 else ''
        info_rows = response.xpath('//div[@class="info"]/ul/li/text()[re:test(.,"\\S")]')
        len_info_rows = len(info_rows)

        born_date = ''
        if len_info_rows > 0:
            born_date = info_rows[0].re(r'\d{1,2}\.\d{1,2}\.\d{4}')
            born_date = born_date[0] if len(born_date) > 0 else ''
        born_city = ''
        born_state = ''
        if len_info_rows > 1:
            tokens = info_rows[1].get().strip().split(', ')
            if len(tokens) > 1:
                born_city = tokens[0]
                born_state = tokens[-1]

        death_date = ''
        if len_info_rows > 2:
            death_date = info_rows[2].re(r'\d{1,2}\.\d{1,2}\.\d{4}')
            death_date = death_date[0] if len(death_date) > 0 else ''
        death_city = ''
        death_state = ''
        if len_info_rows > 3:
            tokens = info_rows[3].get().strip().split(', ')
            if len(tokens) > 1:
                death_city = tokens[0]
                death_state = tokens[-1]
        return ParticipantItem(
            name=name,
            photo=photo,
            bornDate=born_date,
            bornCity=born_city,
            bornState=born_state,
            deathDate=death_date,
            deathCity=death_city,
            deathState=death_state,
            url=url
        )

