Clash of Clans API client
===========================================================

Simple yet complete Python client for ClashOfClans API.

The design phylosophy is use the same structure in the API call and the REST Url. 
So reading the official API documentation, client calls become intuitive.

== Installation ==   

It is available using pip. Simply type:

    pip install coc-client

== Using the client ==
  
Create a new Clash of clans connector.
Use the API key as the `bearer_token` to identify your call.

To start the client:
        
    from coc import ClashOfClans 
    coc = ClashOfClans(bearer_token=<api_key>)

To access simple URL, for instance to request all locations (GET /locations) use 

    r = coc.locations.get()

The `locations` attribute sets the uri part (with the same name), and the `get` method executes the http call.
An analogous method named `post` executes a POST request instead of an GET request.

To URLs with parameters, for instance requesting a particular location given by an id (GET /locations/{locationId}) use

    r = coc.locations(32000218).get()

To access the rankings of a location (GET /locations/{locationId}/rankings/{rankingId})

    r = coc.locations(32000218).rankings('clans').get()
    r = coc.locations(32000218).rankings.clans.get()

To include parameters in the call provide dictionary like arguments to the call:

    coc.clans(name='theclan', minMembers=10).get()

This produces /clans?name=theclan&minMembers=10. The parameters are uri encoded.

Note that attributes starting with an underscore are omitted.

== Response wrappers ==

The response of ClashOfClans API calls is of type `ApiRespose`. 
It wrappes either a `list` or a `dict`, depending on the nature of the object contained.
The contained object is the result of decoding the JSON string obtained as response.

For instance, locations returns a list of locations:

    r = coc.locations.get()
    r[0]['nane'] # r is a list
    >> "Europe"

While, getting a location by id returns a single objcet, this is a dict:

    coc.locations(32000000).get()
    >>> {
      "id": 32000000,
      "name": "Europe",
      "isCountry": false
    }

It is important to point out that the API never returns a list as a root object. 
When a list is returned it is wrapped in a dictionary with the key `items`. 
The ClashOfClans client will passe the response and extract the items list, and return it as response.
In case this behaviour is not desired, the parameter `extract_items` should be set to `False` when creating the `ClashObClans` client.

=== Additional information ===

Response objects also contain additional information about the response. This is:

* the response headers, in the `headers` attribute.
* the status code, given by the `status_code` attribute. 
* the error message, stored in the `error` attribute.


== Further configuration ==

ClashOfClans constructor provides additional configuration:

* endpoint: to set the endpoint to use. By default it uses `https://api.clashofclans.com`. 
* api_version: used to build the URI to request. By default is is set to `v1`.
* extract_items: set to `True` to parse the response and extract the items. When set to `False` the response is returned as got from requests library.

== Contributions and development ==

Contributions are welcome. Simply clone or fork the repo, or open an issu to discuss about bugs and features.

All library requirements are provided in the `requirements.txt` file. Additiolan requirements for testing are gathered in the `test-requirements.txt` file.  

To run the tests locally, the COC_API_KEY environment variable must be set. 