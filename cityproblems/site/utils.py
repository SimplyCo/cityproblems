# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from cityproblems.admin.models import SiteParameters

import re
import sys


def get_map_center():
    center = dict()
    try:
        center["latitude"] = SiteParameters.objects.only("value").get(key="latitude").value
        center["longitude"] = SiteParameters.objects.only("value").get(key="longitude").value
        center["zoom"] = SiteParameters.objects.only("value").get(key="zoom").value
    except ObjectDoesNotExist:
        center["latitude"] = "50.444388"
        center["longitude"] = "30.562592"
        center["zoom"] = 11
    return center


def get_safe_url_name(text):
    if sys.version_info.major == 3:
        text = text.lower().replace(" ", "_")
    else:
        text = str(text.encode('utf-8')).lower().replace(" ", "_")
    p = re.compile(r"^[a-z0-9_]+$")
    if p.search(text):
        return text
    matches = {u"а":"a",u"б":"b",u"в":"v",u"г":"g",u"ґ":"g",u"д":"d",u"е":"e",u"ё":"yo",u"є":"ye",u"ж":"zh",u"з":"z",u"и":"y",u"і":"i",u"ї":"yi",u"й":"j",u"к":"k",u"л":"l",u"м":"m",u"н":"n",u"о":"o",u"п":"p",u"р":"r",u"с":"s",u"т":"t",u"у":"u",u"ф":"f",u"х":"x",u"ц":"cz",u"ч":"ch",u"ш":"sh",u"щ":"shh",u"ю":"yu",u"я":"ya"}
    result = str()
    for i in text:
        ch = matches.get(i, None)
        if ch is not None and p.search(ch):
            result += ch
        elif p.search(i):
            result += i
    return result
