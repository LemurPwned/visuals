import scrapy

import datetime


class Event():
    def __init__(self, name, start_date, stop_date, place):
        self.name = name
        self.start_date = start_date
        self.stop_date = stop_date
        self.place = place


class EventScrap(scrapy.Spider):
    name = "event"

    def start_requests(self):
        year = 2019
        month = 3
        start_day = 10
        stop_day = 10
        start_date = datetime.datetime(year, month, start_day)
        end_date = datetime.datetime(year, month, stop_day)
        step = datetime.timedelta(days=1)

        base_url = 'http://www.krakow.pl/kalendarium/1919,shw,'
        urls = []
        while start_date <= end_date:
            urls.append(
                f"{base_url}{start_date.strftime('%Y-%m-%d')},day.html")
            start_date += step
            yield scrapy.Request(url=f"{base_url}{start_date.strftime('%Y-%m-%d')},day.html", callback=self.parse_day_events)

    def parse_event_page(self, response):
        place_tag = response.xpath(
            '/html/body/div[8]/div[1]/div[2]/div/div[2]/div/div[3]/div/div[3]/div[2]/strong/text()').get()
        category_tag = response.xpath(
            '/html/body/div[8]/div[1]/div[2]/div/div[2]/div/div[3]/div/div[4]/div[2]/strong/text()').get()
        yield {'category': category_tag, 'place': place_tag}

    def parse_day_events(self, response):
        events_xpath = '/html/body/div[8]/div[1]/div[2]/div/div[2]/div/div[3]/div[3]'
        c = 1
        row = response.xpath(events_xpath)
        for row in response.xpath(events_xpath).css('div.row'):
            event_name = row.css('a.list_title::text').get().strip()
            event_date = row.css('div.row div.list_title_row div.list_head div.list_data::text').get(
            ).strip().replace('\n', '').replace(' ', '')
            event_href = row.css('div.row a::attr(href)').get()
            print(
                f"Requested: {event_name, event_date}")
            yield response.follow(
                f"http://www.krakow.pl/{event_href}", self.parse_event_page, meta={
                    'event_date': event_date, 'event_name': event_name
                })
            # event_names = row.css('div.row a.list_title::text').getall()
            # event_hrefs = row.css(
            #     'div.row a::attr(href)').getall()
            # event_dates = row.css(
            #     'div.row div.list_title_row div.list_head div.list_data::text').getall()
            # assert len(event_dates) == len(event_dates)
            # event_names = list(map(lambda x: x.strip(), event_names))
            # event_dates = list(map(lambda x: x.strip().replace(
            #     '\n', '').replace(' ', ''), event_dates))
            # print(event_names)
            # for href in event_hrefs:
            #     yield response.follow(
            #         f"http://www.krakow.pl/{href}", self.parse_event_page)
        # yield {'events': event_names, 'dates': event_dates, ''}
