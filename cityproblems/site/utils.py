from django.core.exceptions import ObjectDoesNotExist

from cityproblems.admin.models import SiteParameters


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