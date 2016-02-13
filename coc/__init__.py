"""
Clash of clans API client
"""

from textwrap import dedent

from .api import ClashOfClans, ApiCall, ApiResponse
from .utils import filter_country_locations


__doc__ = __doc__ or ""

__doc__ += """
The ClashOfClans class
-----------------
"""
__doc__ += dedent(ClashOfClans.__doc__ or "")



___all__= ["filter_country_locations",
           "ClashOfClans", 
           "ApiCall", 
           "ApiResponse"]