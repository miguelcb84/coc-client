ISCOUNTRY = 'isCountry'

def filter_country_locations(api_response, is_country=True):
    """ 
    Filter the response to only include the elements that are countries. 
    
    This uses the 'api_response' object as input. Plain `list`s are also 
    valid, but they must contain the location elements, not the `items` wrapper. 
    """
    return [item for item in api_response if item[ISCOUNTRY]==is_country]        

   
__all__= ['filter_country_locations']