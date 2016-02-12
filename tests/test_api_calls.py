from coc.api import ClashOfClans
from os import environ
import pytest

@pytest.fixture
def api_key():
    return environ['COC_API_KEY']


slow_test = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

@slow_test
@pytest.mark.api_call
def test_locations_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.locations.get()
    assert r.status_code == 200
    assert isinstance(r, list)

@slow_test
@pytest.mark.api_call    
def test_specific_locations_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.locations(32000260).get()
    assert r.status_code == 200
    assert isinstance(r, dict)
    assert r['countryCode'] == u'ZW'
    assert r['id'] == 32000260
    assert r['isCountry'] == True
    assert r['name'] == u'Zimbabwe'

@slow_test 
@pytest.mark.api_call    
def test_location_clan_rank_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.locations(32000260).rankings.clans.get()
    assert r.status_code == 200

@slow_test
@pytest.mark.api_call
def test_location_player_rank_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.locations(32000260).rankings.clans.get()
    assert r.status_code == 200
    
@slow_test
@pytest.mark.api_call
def test_leagues_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.leagues.get()
    assert r.status_code == 200
    assert isinstance(r, list)

@slow_test
@pytest.mark.api_call
def test_clan_by_tag_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.clans('#8R9LRVGU').get()
    assert r.status_code == 200
    assert isinstance(r, dict)
    
@slow_test
@pytest.mark.api_call
def test_clan_members_by_tag_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.clans('#8R9LRVGU').members.get()
    assert r.status_code == 200
    assert isinstance(r, list)
    
@slow_test
@pytest.mark.api_call
def test_clan_search_apicall(api_key):
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.clans(minMembers=10).get()
    assert r.status_code == 200
    assert isinstance(r, list)
    
    coc = ClashOfClans(bearer_token=api_key)
    r = coc.clans(minMembers=10, warFrequency='always').get()
    assert r.status_code == 200
    assert isinstance(r, list)