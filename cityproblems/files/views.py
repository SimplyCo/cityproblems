#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from annoying.decorators import ajax_request
from cityproblems.site.models import *
from .forms import *

import json

User = get_user_model()


@ajax_request
def process_upload(request):
    if not request.user.is_authenticated():
        return {"Error": _("Login please")}
    if request.method != "POST":
        return HttpResponse("Use post")
    try:
        problem = Problem.objects.get(id=request.POST.get("id"))
    except ObjectDoesNotExist:
        return {"Error": _("No such object")}
    if not problem.is_can_edit(request.user):
        return {"Error": _("Permission denied")}
    form = ImageValidationForm(request.POST, request.FILES)
    if not form.is_valid():
        return {"Error": form.errors.get("file")}
    file = ProblemImage()
    if request.FILES.get("file") is None:
        return {"Error": _("No file")}
    else:
        file.thumbnail = request.FILES.get("file")  # todo thumbnail here
        file.small_image = request.FILES.get("file")
        file.medium_image = request.FILES.get("file")
        file.big_image = request.FILES.get("file")
    file.problem = problem
    order_number = problem.problemimage_set.all().order_by("-order_number").values_list("order_number")[:1]
    if not order_number:
        order_number = 1
    else:
        order_number = order_number[0][0] + 1
    file.order_number = order_number
    file.save()
    return {"id": file.id, "url": file.big_image.url,
            "thumbnail": file.thumbnail.url, "order_number": file.order_number}


@ajax_request
def process_file_remove(request):
    if not request.user.is_authenticated():
        return {"Error": _("Login please")}
    if request.method != "POST":
        return HttpResponse("Use post")
    try:
        body = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return {"Error": "Error"}
    try:
        file = ProblemImage.objects.get(id=body.get("id"))
    except ObjectDoesNotExist:
        return {"Error": _("No such file")}
    if not file.problem.is_can_edit(request.user):
        return {"Error": _("Permission denied")}
    file.delete()
    return {"Ok": "Ok"}


@ajax_request
def process_image_move(request):
    if request.method != 'POST':
        return HttpResponse("Use post")
    try:
        body = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return {'Error': "Error: can`t parse message"}
    id = body.get('id', 0)
    action = body.get('action', 0)
    try:
        action = int(action)
    except ValueError:
        return {'Error': "Wrong parameter"}
    try:
        object = ProblemImage.objects.get(id=id)
    except ObjectDoesNotExist:
        return {'Error': "No such option"}
    if not object.problem.is_can_edit(request.user):
        return {"Error": "Permission denied"}
    if action < 0:
        swapObject = ProblemImage.objects.filter(order_number__lt=object.order_number).order_by("-order_number")\
            .only("order_number")[:1]
    elif action > 0:
        swapObject = ProblemImage.objects.filter(order_number__gt=object.order_number).only("order_number")[:1]
    else:
        return {'Error': "Wrong parameter"}
    if not len(swapObject):
        return {'Error': "Wrong action"}
    swapObject = swapObject[0]
    swapObject.order_number += object.order_number
    object.order_number = swapObject.order_number - object.order_number
    swapObject.order_number -= object.order_number
    object.save()
    swapObject.save()
    return {"ok": "ok"}
