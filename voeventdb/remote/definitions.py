"""
Define the keys / values used in querystrings that are same across API-versions.
"""

class PaginationKeys:
    limit = 'limit'
    offset = 'offset'
    order = 'order'

class ResultKeys:
    endpoint = 'endpoint'
    limit = 'limit'
    querystring = 'querystring'
    result = 'result'
    url = 'url'
