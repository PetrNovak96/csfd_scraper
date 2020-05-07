import scrapy


class FilmItem(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    rating = scrapy.Field()
    duration = scrapy.Field()
    year = scrapy.Field()
    comments_count = scrapy.Field()
    genre = scrapy.Field()
    record_type = scrapy.Field()
    url = scrapy.Field()


class ParticipantItem(scrapy.Item):
    name = scrapy.Field()
    photo = scrapy.Field()
    bornDate = scrapy.Field()
    bornCity = scrapy.Field()
    bornState = scrapy.Field()
    deathDate = scrapy.Field()
    deathCity = scrapy.Field()
    deathState = scrapy.Field()
    url = scrapy.Field()


class ParticipationItem(scrapy.Item):
    film_url = scrapy.Field()
    participant_url = scrapy.Field()
    type = scrapy.Field()