# -*- coding: utf-8 -*-
try:
    from urlparse import urlparse
except ImportError:
    # python3
    from urllib.parse import urlparse


def nextPage(GET, notExist='/'):
    if 'next' in GET:
        url = GET['next']
        url = urlparse(url).path
    else:
        url = notExist
    return url
