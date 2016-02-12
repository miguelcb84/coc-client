from coc.api import ClashOfClans, build_uri
import pytest

## REST API CALLS
def test_locations_apicall_url():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.locations
    assert 'locations' in apicall.uri_parts
    assert len(apicall.uri_parts) == 1

def test_location_by_id_apicall_url():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.locations(123)
    assert 'locations' in apicall.uri_parts
    assert 123 in apicall.uri_parts
    assert len(apicall.uri_parts) == 2

def test_locations_rankings_apicall_url():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.locations(123).rankings.clans
    assert 'locations' in apicall.uri_parts
    assert 123 in apicall.uri_parts
    assert 'rankings' in apicall.uri_parts
    assert 'clans' in apicall.uri_parts
    assert len(apicall.uri_parts) == 4
    
    apicall = coc.locations(123).rankings('clans')
    assert 'locations' in apicall.uri_parts
    assert 123 in apicall.uri_parts
    assert 'rankings' in apicall.uri_parts
    assert 'clans' in apicall.uri_parts
    assert len(apicall.uri_parts) == 4
    
    apicall = coc.locations(123).rankings.players
    assert 'locations' in apicall.uri_parts
    assert 123 in apicall.uri_parts
    assert 'rankings' in apicall.uri_parts
    assert 'players' in apicall.uri_parts
    assert len(apicall.uri_parts) == 4

    apicall = coc.locations(123).rankings('players')
    assert 'locations' in apicall.uri_parts
    assert 123 in apicall.uri_parts
    assert 'rankings' in apicall.uri_parts
    assert 'players' in apicall.uri_parts
    assert len(apicall.uri_parts) == 4

def test_clans_by_id_apicall_url():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.clans('#8R9LRVGU')
    assert 'clans' in apicall.uri_parts
    assert '#8R9LRVGU' in apicall.uri_parts
    assert len(apicall.uri_parts) == 2

def test_clans_members_apicall_url():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.clans('#8R9LRVGU').members
    assert 'clans' in apicall.uri_parts
    assert '#8R9LRVGU' in apicall.uri_parts
    assert 'members' in apicall.uri_parts
    assert len(apicall.uri_parts) == 3
    
def test_leagues_apicall_url():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.leagues
    assert 'leagues' in apicall.uri_parts
    assert len(apicall.uri_parts) == 1

## REST API CALLS WITH PARAMS
def test_clans_apicall_url():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.clans(name='pupus',minMembers=10)
    assert 'name' in apicall.uri_args
    assert apicall.uri_args['name'] == 'pupus'
    assert 'minMembers' in apicall.uri_args
    assert apicall.uri_args['minMembers'] == 10
    
## build_uri funtion
def test_build_uri():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.locations('123').rankings('players')
    built_uri = build_uri(coc.endpoint, coc.api_version, apicall.uri_parts)
    assert built_uri == 'http://endpoint/v0/locations/123/rankings/players'
    
    apicall = coc.locations('123').rankings.clans
    built_uri = build_uri(coc.endpoint, coc.api_version, apicall.uri_parts)
    assert built_uri == 'http://endpoint/v0/locations/123/rankings/clans'

def test_build_uri_scaping_chars():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.clans('#8R9LRVGU').members
    built_uri = build_uri(coc.endpoint, coc.api_version, apicall.uri_parts)
    assert built_uri == 'http://endpoint/v0/clans/%238R9LRVGU/members'
    
def test_build_uri_with_parameters():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.clans(name='pupus',minMembers=10)
    built_uri = build_uri(coc.endpoint, coc.api_version, apicall.uri_parts, apicall.uri_args)
    assert built_uri == 'http://endpoint/v0/clans?name=pupus&minMembers=10' or built_uri == 'http://endpoint/v0/clans?minMembers=10&name=pupus'
    
def test_build_uri_with_parameters_scape_chars():
    coc = ClashOfClans(bearer_token="fake_key", endpoint="http://endpoint", api_version="v0")
    apicall = coc.clans(name='you=too',warFrequency='always')
    built_uri = build_uri(coc.endpoint, coc.api_version, apicall.uri_parts, apicall.uri_args)
    assert built_uri == 'http://endpoint/v0/clans?name=you%3Dtoo&warFrequency=always' or built_uri == 'http://endpoint/v0/clans?warFrequency=always&name=you%3Dtoo' 
