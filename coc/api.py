# encoding: utf-8
from __future__ import unicode_literals, print_function
import requests
import urllib


def build_uri(endpoint, api_version, uri_parts, uri_args={}):
    """ Build the URL using the endpoint, the api version, the uri parts and the args.
    
        :param dict uri_args: parameters to include in the URL. 
        :param tuple uri_parts: url encoded and `uri_parts` too.
        :return: A string that represents the absolute URL of the request
        :rtype : str
    
        The resulting uri is as follows:
    
        {endpoint}/{api_version}/{uri_part1}/.../{uri_partn}?{uri_args}
        
        The `uri_args` and the `uri_parts` are url encoded.
    """
    # to unicode
    uri_parts = [str(x) for x in uri_parts]
    # and encoded 
    uri_parts = [urllib.parse.quote(x) for x in uri_parts]
    # Add enpoint and version 
    all_uri_parts = [endpoint, api_version, ] + uri_parts
    # join parts
    url_to_call = "/".join(all_uri_parts)
    # add params if any
    if uri_args:
        url_to_call = "{}?{}".format(url_to_call, urllib.urlencode(uri_args))
    # return
    return url_to_call


def wrap_response(resp, api_call):
    """ Wrap the requests response in an `ApiResponse` object 
    
        :param object resp: response object provided by the `requests` library.
        :param object api_call: Api Call
        :return: An `ApiResponse` object that wraps the content of the response.
        :rtype: object, list or dict
    """
    try:
        js_resp = resp.json()
        if resp.ok:
            if "items" in js_resp.keys():
                r = ApiListResponse(js_resp["items"])
            else:
                r = ApiDictResponse(js_resp)
            if "paging" in js_resp.keys():
                cursors = js_resp.get("paging", {}).get("cursors", {})
                if "after" in cursors.keys():
                    r.next = api_call(after=cursors["after"])
                if "before" in cursors.keys():
                    r.previous = api_call(after=cursors["before"])
        else:
            r = ApiDictResponse(js_resp)
            if "error" in js_resp.keys():
                r.error = js_resp['error']
            elif "message" in js_resp.keys():
                r.error = js_resp['message']
        # common to all
        r.status_code = resp.status_code 
        r.headers = resp.headers
        return r
    except:
        return resp


class ApiResponse():
    pass


class ApiListResponse(list, ApiResponse):
    pass


class ApiDictResponse(dict, ApiResponse):
    pass
    

class ApiCall(object):
    """ Minified REST API call generator using attributes.
    
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
            
        The way it works, it that each access to `ApiCall` attributes returns a 
        new API call with the attributtes with the existing one, but it appends
        the uri part. Sequential call, thus produce the explained result.
        
        Note that attributes starting with an underscore are omitted.
        
        Additionally, arguments are supported. To use them you must provide dictionary like parameters:
        
            api.clans(name='theclan', minMembers=10)
    """
    
    def __init__(self, bearer_token, endpoint, api_version, 
                 extract_items=True, uri_parts=None, uri_args={}):
        """ Construct an ApiCall object.
        
            :param str bearer_token: the API key provided 
            :param str endpoint: The endpoint od the API
            :param str api_version: The version of the API. Used to build the API url
            :param boolean extract_items: If true, response will be parsed and wraped 
                in a list or dictionary. Otherwise, the requests response will be 
                returned. 
            :param tuple uri_parts: Provide an initial value to uri_parts. Used with 
                recursive calls by the `__getattr__` and `__call__` methods. 
            :param dict uri_args: arguments of the call. 
        """
        self.bearer_token = bearer_token
        self.endpoint = endpoint
        self.api_version = api_version
        self.extract_items=extract_items
        self.uri_args=uri_args
        if uri_parts is None:
            self.uri_parts = ()
        else:
            self.uri_parts = uri_parts
    
    def __getattr__(self, k):
        """ Append the name of the attribute to the uri_parts tuple. 
            Attributes starting with an underscore are omitted. `self` is returned 
            to enable chainability. 
        """
        if k.startswith("_"):
            pass
        else:
            return ApiCall(self.bearer_token, self.endpoint, self.api_version, extract_items=self.extract_items,
                           uri_parts=self.uri_parts + (k,), uri_args=self.uri_args)
                    
    def __call__(self, *args, **kwargs):
        """ Append the arguments to the `uri_parts` tuple. `self` is returned 
            to enable chainability. 
        """
        if args or kwargs:
            uri_args = {}
            if kwargs:
                uri_args = self.uri_args.copy()
                uri_args.update(kwargs)
            
            return ApiCall(self.bearer_token, self.endpoint, self.api_version, extract_items=self.extract_items,
                           uri_parts=self.uri_parts + args, uri_args=uri_args)
        return self

    def build_headers(self):
        """ Build the required headers to make the API call """
        return {"Accept": "application/json", "authorization": "Bearer {}".format(self.bearer_token)}

    def _process_call(self, method):
        url = build_uri(self.endpoint, self.api_version, self.uri_parts, self.uri_args)
        r = requests.get(url, headers=self.build_headers())
        #self.uri_parts = ()
        if self.extract_items:
            return wrap_response(r, self)
        else:
            return r 
      
    def get(self):
        ''' Execute a GET API call given by the `uri_parts` stored.'''
        return self._process_call('get')
        
    def post(self):
        ''' Execute a POST API call given by the `uri_parts` stored.'''
        return self._process_call('post')

    
class ClashOfClans(ApiCall):
    """ Create a new Clash of clans connector.
    
        Use the `bearer_token` to identify your call.
        
        `endpoint` lets you change the api endpoint which is used to build the base URI. 
         By default is uses 'https://api.clashofclans.com'.
        
        `api_version` is used to build the base URI. By default it uses 'v1'.
        
        Examples:
        
            To start the client:
                
                from coc import *
                coc = ClashOfClans(bearer_token=<api_key>)
        
            To access all locations use the call (GET /locations)
            
                coc.locations.get()
            
            To access a particular location given by an id (GET /locations/{locationId})
            
                coc.locations(32000218).get()
            
            To access the rankings of a location GET /locations/{locationId}/rankings/{rankingId}
            
                coc.locations(32000218).rankings('clans').get()
                coc.locations(32000218).rankings.clans.get()
            
            Note that attributes starting with an underscore are omitted.
            
            To include parameters in the call use provide dictionary like arguments to the call:
        
                coc.clans(name='theclan', minMembers=10).get()
            
            This produces /clans?name=theclan&minMembers=10. The parameters are uri encoded.
            
            When the results are split in more than one page (for instance, when we limit 
            the number of results using the `limit` param) pagination is automatically 
            handled by the client. In those cases the response will contain a `next` and ` previous` 
            attributes to store the `ApiCall` objects to get the next and the previous page. 
            For instance:
            
                r = coc.clans(nam='myclan', limit=5).get()
                r.next # contains the next api call to use
                r2 = r.next.get() # returns the second page
        
    """
    def __init__(self, 
                 bearer_token,
                 endpoint='https://api.clashofclans.com', 
                 api_version='v1',
                 extract_items=True):
        """ Contruct a ClashOfClans client.
        
            :param str bearer_token: the AP key provided by CoC 
            :param str endpoint: the endpoint of the API. Default value is https://api.clashofclans.com 
            :param str api_version: the version of the API. Default value is v1
            :param boolean extract_items: if True, the response will be parsed and wraped in a list or 
                    dictionary. Otherwise, the requests response will be returned.
        """
        super(ClashOfClans, self).__init__(
            bearer_token=bearer_token,
            endpoint=endpoint,
            api_version=api_version,
            extract_items=extract_items, 
            uri_parts=None)
    
    
___all__= ["ClashOfClans", "ApiCall", "ApiResponse"]
