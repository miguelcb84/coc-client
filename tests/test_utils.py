from coc.utils import filter_country_locations
import pytest

@pytest.fixture
def response_api_locations():
    return [
        {'id': 32000000, 'isCountry': False, 'name': 'Europe'},
        {'id': 32000001, 'isCountry': False, 'name': 'North America'},
        {'countryCode': 'AF',
          'id': 32000007,
          'isCountry': True,
          'name': 'Afghanistan'},
         {'countryCode': 'AX',
          'id': 32000008,
          'isCountry': True,
          'name': '\xc5land Islands'},
         {'countryCode': 'AL',
          'id': 32000009,
          'isCountry': True,
          'name': 'Albania '}
    ]

def test_filter_country_locations__filters_countries(response_api_locations):
    assert len(filter_country_locations(response_api_locations)) == 3
    assert len(filter_country_locations(response_api_locations, is_country=True)) == 3
    
def test_filter_country_locations__filters_not_countries(response_api_locations):
    assert len(filter_country_locations(response_api_locations, is_country=False)) == 2