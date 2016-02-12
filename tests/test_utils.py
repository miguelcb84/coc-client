from coc.utils import filter_country_locations
import pytest

@pytest.fixture
def response_api_locations():
    return [
        {u'id': 32000000, u'isCountry': False, u'name': u'Europe'},
        {u'id': 32000001, u'isCountry': False, u'name': u'North America'},
        {u'countryCode': u'AF',
          u'id': 32000007,
          u'isCountry': True,
          u'name': u'Afghanistan'},
         {u'countryCode': u'AX',
          u'id': 32000008,
          u'isCountry': True,
          u'name': u'\xc5land Islands'},
         {u'countryCode': u'AL',
          u'id': 32000009,
          u'isCountry': True,
          u'name': u'Albania '}
    ]

def test_filter_country_locations__filters_countries(response_api_locations):
    assert len(filter_country_locations(response_api_locations)) == 3
    assert len(filter_country_locations(response_api_locations, is_country=True)) == 3
    
def test_filter_country_locations__filters_not_countries(response_api_locations):
    assert len(filter_country_locations(response_api_locations, is_country=False)) == 2