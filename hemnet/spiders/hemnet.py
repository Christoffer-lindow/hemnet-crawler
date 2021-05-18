import scrapy
from pydispatch  import dispatcher
import codecs
from scrapy import signals
import time
import json

class HemnetSpider(scrapy.Spider):
    name = "hemnet"
    start_urls = ["https://www.hemnet.se/bostader?location_ids%5B%5D=17919&item_types%5B%5D=bostadsratt",
    "https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17919&page=2",
    "https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17919&page=3"
    ]
    estate_entries = []
    
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    

    def parse(self,response):
        for line in response.css("ul.normal-results > li.normal-results__hit > a::attr('href')"):
            time.sleep(3)
            yield scrapy.Request(url=line.get(), callback=self.parse_inner)
        
    
    def parse_inner(self, response):
        time.sleep(2)
        property_entry = dict()
        property_entry["url"] = response.request.url
        property_entry["img-url"] = response.css("img.property-gallery__item::attr('src')").get()
        property_entry["street"] = response.css("h1.qa-property-heading::text").get()
        property_entry["address"] = response.css("span.property-address__area::text").get()
        property_entry["price"] = int(response.css("p.property-info__price::text").get().replace("kr","").replace(u"\xa0", ""))

        for attrs in response.css("div.property-attributes > div.property-attributes-table > dl.property-attributes-table__area > div.property-attributes-table__row"):
            attr_key = attrs.css("dt.property-attributes-table__label::text").get()
            attr_val = attrs.css("dd.property-attributes-table__value::text").get()
            
            if attr_val is not None:
                attr_val = attr_val.replace(u"\n", "")
                attr_val = attr_val.replace(u"\t", "")
                attr_val = attr_val.replace(u"\xa0", "")
                attr_val = attr_val.replace("kr/m²", "")
                attr_val = attr_val.replace("kr/år", "")
                attr_val = attr_val.replace("kr/mån", "")
                attr_val = attr_val.replace("m²", "")
                attr_val = attr_val.strip()
            if attr_key is not None:
                attr_key = attr_key.replace(u"\n", "")
                attr_key = attr_key.replace(u"\t","")
                attr_val = attr_val.replace(u"\xa0", "")
                attr_key = attr_key.strip()
            
            if attr_key is not None:
                property_entry[attr_key] = attr_val
        self.estate_entries.append(property_entry)
    
    def spider_closed(self, spider):
        with open('data.json',  'w') as fp:
            json.dump(self.estate_entries, fp)