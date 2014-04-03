#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import base64

from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.translation import ugettext as _
from annoying.decorators import render_to

from .models import *
from .forms import *
from cityproblems.admin.models import SiteParameters


@render_to('site/index.html')
def home(request):
    form = AuthenticationForm()
    return {
        'form': form,
    }


@render_to('site/no_permissions.html')
def no_permissions(request):
    return {}


@login_required
@render_to('site/site_user_cabinet.html')
def user_cabinet(request):
    return {}


@login_required
def create_problem(request):
    problem = Problem.objects.create(author=request.user)
    return HttpResponseRedirect(reverse("site_add_problem", args=(problem.id,)))


@login_required
@render_to('site/site_new_problem_form.html')
def edit_problem(request, id):
    problem = get_object_or_404(Problem, id=id)
    if not problem.is_can_edit(request.user):
        return HttpResponseRedirect(reverse("no_permissions"))
    form = ProblemEditForm(request.POST or None, instance=problem)
    if form.is_valid():
        form.save()
        messages.success(request, _("Changes saved"))
        return HttpResponseRedirect(reverse("site_user_cabinet"))
    center = dict()
    try:
        center["latitude"] = SiteParameters.objects.only("value").get(key="latitude").value
        center["longitude"] = SiteParameters.objects.only("value").get(key="longitude").value
        center["zoom"] = SiteParameters.objects.only("value").get(key="zoom").value
    except ObjectDoesNotExist:
        center["latitude"] = "50.444388"
        center["longitude"] = "30.562592"
        center["zoom"] = 11
    files = base64.standard_b64encode(json.dumps(problem.get_images()))
    return {"form": form, "center": center, "problem": problem, "files": files}
