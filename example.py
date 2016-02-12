from coc.api import ClashOfClans
from os import environ


if __name__ == '__main__':
    api=ClashOfClans(environ['COC_API_KEY'])
    print api.locations(32000183).get()