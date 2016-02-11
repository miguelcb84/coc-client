# encoding: utf-8
from __future__ import unicode_literals, print_function
import ipdb
import requests
    

def build_uri(endpoint, api_version, uri_parts):
    ''' Build the URL using the endpoint, the api version and the uri parts '''
    all_uri_parts = (endpoint, api_version, ) + uri_parts
    url_to_call = "/".join(all_uri_parts)
    return url_to_call


class ApiResponse():
    pass


class ApiListResponse(list, ApiResponse):
    pass


class ApiDictResponse(dict, ApiResponse):
    pass
    

class ApiCall(object):
    ''' 
    Minified REST API call generator using attributes.
    
    REST URLs are replicated using properties and method calls as shown. 
    The URI path:
        
        /locations/12003/rank/global
    
    Is replicated using sequence:
        
        api.locations(12003).rank.global
        
    In order make the api call, the methods `get` and `post` are provided 
    (each using a different http method). In the call, the endpoint and the 
    version of the api are included as the URL base. So, a sequence:
    
        api=ApiCall(endpoint='http://example.org', api_version='v1')
        api.locations(12003).rank.global.get()
        
    Will perform an http get to the URL:
    
        http://example.org/v1/locations/12003/rank/global
        
    The way it works, it that each access to `ApiCall` properties appends an 
    additional uri part which are accumulated in the `uri_parts` attribute. 
    These are not required to be in concatenaded. Thus, the followin call is 
    identical to the formar one:
    
        api.locations(12003)
        api.rank.global
        api.get()
    
    Once `get` or `post` methods are called, the accumulated uri parts are 
    cleared, to let different api calls be executed.
    '''
    
    def __init__(self, bearer_token, endpoint, api_version, uri_parts=None):
        ''' Tranfer provided aruments and initialize `uri_parts` attribute '''
        self.bearer_token = bearer_token
        self.endpoint = endpoint
        self.api_version = api_version
        self.uri_parts = ()
    
    def __getattr__(self, k):
        ''' Append the name of the attribute to the uri_parts tuple. 
        Attributes starting with an underscore are omitted. `self` is returned 
        to enable chainability. '''
        print("GETATTR:{}".format(k))
        if k.startswith("_"):
            pass
        else:
            self.uri_parts = self.uri_parts + (k,)
            return self
                    
    def __call__(self, *args, **kwargs):
        ''' Append the arguments to the `uri_parts` tuple. `self` is returned 
        to enable chainability. '''
        print('CALL:{}'.format(args))
        if args:
            self.uri_parts = self.uri_parts + args
        return self

    def build_headers(self):
        return {"Accept": "application/json", "authorization": "Bearer {}".format(self.bearer_token)}

    def _process_call(self, method):
        url = build_uri(self.endpoint, self.api_version, self.uri_parts)
        r = requests.get(url, headers=self.build_headers)
        self.uri_parts = ()
        return r.content
      
    def get(self):
        ''' Execute a GET API call given by the `uri_parts` stored.'''
        return self._process_call('get')
        
    def post(self):
        ''' Execute a POST API call given by the `uri_parts` stored.'''
        return self._process_call('post')

    
class ClashOfClans(ApiCall):
    """ 
    Create a new Clash of clans connector.
    
    Use the `bearer_token` to identify your call.
    
    `endpoint` lets you change the api endpoint which is used to build the base URI. 
     By default is uses 'https://api.clashofclans.com'.
    
    `api_version` is used to build the base URI. By default it uses 'v1'.
    """
    
    def __init__(self, 
                 bearer_token,
                 endpoint='https://api.clashofclans.com', 
                 api_version='v1'):
        
        self.bearer_token = bearer_token
        self.endpoint = endpoint
        self.api_version = api_version
    
