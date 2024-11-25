import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class PropertySpider(CrawlSpider):
    name = "property"
    start_urls = ["https://www.bproperty.com/buy/dhaka/rampura/"]

    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@class="ListingCell-AllInfo ListingUnit"]/a'), callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths='//div[@class="next "]/a'),follow=True),
             )

    def parse_item(self, response):
        text = response.text



        # Regex patterns to capture latitude and longitude values
        latitude_pattern = r'"location_latitude":\s*"([0-9.\-]+)"'
        longitude_pattern = r'"location_longitude":\s*"([0-9.\-]+)"'

        # Extract latitude and longitude
        latitude = re.search(latitude_pattern, text)
        longitude = re.search(longitude_pattern, text)

        # Output results
        latitude_value = latitude.group(1) if latitude else None
        longitude_value = longitude.group(1) if longitude else None

        # Regular expressions for each field
        date_pattern = r'"date":"(.*?)"'
        bedrooms_pattern = r'"bedrooms":(\d+)'
        bathrooms_pattern = r'"bathrooms":(\d+)'
        unit_no_pattern = r'"unit_no":(\d+)'
        floor_no_pattern = r'"floor_no":(\d+)'
        occupancy_status_pattern = r'"occupancy_status":"(.*?)"'
        builtin_year_pattern = r'"builtin_year":(\d+)'
        floor_area_pattern = r'"floor_area":(\d+)'

        # Function to extract data with fallback to None
        def extract_or_none(pattern, text, is_int=False):
            match = re.search(pattern, text)
            if match:
                return int(match.group(1)) if is_int else match.group(1).strip()
            return None

        # Extract data with fallback
        date = extract_or_none(date_pattern, text)
        bedrooms = extract_or_none(bedrooms_pattern, text, is_int=True)
        bathrooms = extract_or_none(bathrooms_pattern, text, is_int=True)
        unit_no = extract_or_none(unit_no_pattern, text, is_int=True)
        floor_no = extract_or_none(floor_no_pattern, text, is_int=True)
        occupancy_status = extract_or_none(occupancy_status_pattern, text)
        builtin_year = extract_or_none(builtin_year_pattern, text, is_int=True)
        floor_area = extract_or_none(floor_area_pattern, text, is_int=True)


        # Regular expression to find all amenities
        amenities_pattern = r'<span class="listing-amenities-name">(.*?)</span>'

        # Find all matches
        amenities = re.findall(amenities_pattern, text)

        


        

        yield{
            'title': response.xpath('//h1[@class="Title-pdp-title"]/span/text()').get().strip(),
            'price': response.xpath('//div[@class="Title-pdp-price"]/span[1]/text()').get().strip(),
            'location': response.xpath('(//h3[@class="Title-pdp-address"]/text())[2]').get().strip(),
            'area': floor_area,
            'published_date': date,
            'bedroom': bedrooms,
            'bathroom': bathrooms,
            'unit_no': unit_no,
            'floor_no': floor_no,
            'occupancy_status': occupancy_status,
            'builtin_year': builtin_year,
            'amenities': amenities,
            'latitude': latitude_value,
            'longitude': longitude_value,
            'url': response.url
        }
