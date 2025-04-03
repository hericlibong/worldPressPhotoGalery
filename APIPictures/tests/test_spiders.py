import os
import pytest
from scrapy.http import HtmlResponse
from APIPictures.spiders.atlantic_pictures import AtlanticPicturesSpider
from APIPictures.spiders.cnn_week_pics import CnnWeekPicsSpider
from APIPictures.spiders.theweek_pictures import TheweekPicturesSpider
from datetime import datetime


def load_fixture(file_name, url):
    # Charger le contennu du fichier de simulation
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        return HtmlResponse(url=url, body=f.read(), encoding='utf-8')
    

# ================ FIXTURES SPÉCIFIQUES PAR SPIDER ================
    
@pytest.fixture
def atlantic_response():
    return load_fixture(
        file_name='atlantic_sample.html',
        url='https://www.theatlantic.com/photo/2025/03/photos-of-the-week-raccoon-snack-tyrannosaurus-race-speed-skiing/682216/'
    ) 

@pytest.fixture
def cnn_response():
    return load_fixture(
        file_name='cnn_sample.html',
        url='https://edition.cnn.com/2025/03/27/world/gallery/photos-this-week-march-20-march-27/index.htmlhttps://edition.cnn.com/world/photos'
    )

@pytest.fixture
def theweek_response():
    return load_fixture(
        file_name='theweek_sample.html',
        url='https://www.theweek.co.uk/gallery/photography/100905/the-week-in-pictures-20-march-2025'
    )

# ================ TESTS CLAIRS POUR CHAQUE SPIDER ================   

def test_atlantic_parse_item(atlantic_response):
    spider = AtlanticPicturesSpider()
    items = list(spider.parse_item(atlantic_response))
    assert len(items) > 0  # Vérifie qu’au moins un item est extrait
    first_item = items[0]

    # Champs principaux dans tous les spiders
    for field in ['media', 'sectionTitle', 'pageUrl', 'pubDate', 'caption', 'author', 'credits', 'picture', 'location', 'pictureEditor']:
        assert field in first_item
        assert first_item[field], f"Le champ {field} ne doit pas être vide."
    
    # champs spécifiques à ce spider
    assert first_item['media'] == "The Atlantic"
    assert first_item['pageUrl'] == atlantic_response.url

    # Vérifie que la date de publication est bien formatée
    datetime.strptime(first_item['pubDate'], '%Y-%m-%d')

def test_cnn_parse_item(cnn_response):
    spider = CnnWeekPicsSpider()
    items = list(spider.parse_item(cnn_response))
    assert len(items) > 0  # Vérifie qu’au moins un item est extrait
    first_item = items[0]

    # Champs principaux dans tous les spiders
    for field in ['media', 'sectionTitle', 'pageUrl', 'pubDate', 'caption', 'author', 'credits', 'picture', 'location', 'pictureEditor']:
        assert field in first_item
        assert first_item[field], f"Le champ {field} ne doit pas être vide."
    
    # champs spécifiques à ce spider
    assert first_item['media'] == "CNN"
    assert first_item['pageUrl'] == cnn_response.url

    # Vérifie que la date de publication est bien formatée
    datetime.strptime(first_item['pubDate'], '%Y-%m-%d')

def test_theweek_parse_item(theweek_response):
    spider = TheweekPicturesSpider()
    items = list(spider.parse_item(theweek_response))
    assert len(items) > 0  # Vérifie qu’au moins un item est extrait
    first_item = items[0]
    # Champs principaux dans tous les spiders
    for field in ['media', 'sectionTitle', 'pageUrl', 'pubDate', 'caption', 'author', 'credits', 'picture', 'location', 'pictureEditor']:
        assert field in first_item
        assert first_item[field], f"Le champ {field} ne doit pas être vide."
    # champs spécifiques à ce spider
    assert first_item['media'] == "theweek"
    assert first_item['pageUrl'] == theweek_response.url
    # Vérifie que la date de publication est bien formatée
    datetime.strptime(first_item['pubDate'], '%Y-%m-%d')

