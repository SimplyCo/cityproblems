#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import base64

from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.translation import ugettext as _
from annoying.decorators import render_to
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.timezone import now

from .models import *
from .forms import *
from cityproblems.admin.models import SiteParameters
from cityproblems.comments.models import Comment

User = get_user_model()


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
def user_cabinet(request, username=None):
    if username is None:
        user = request.user
    else:
        user = get_object_or_404(User, username=username)
    problems = user.problem_set.only("id", "title").exclude(status="creating")
    return {"problems": problems}


@login_required
@render_to('site/site_problem_view.html')
def problem_view(request, id):
    problem = get_object_or_404(Problem, ~Q(status="creating"), id=id)
    try:
        zoom = SiteParameters.objects.only("value").get(key="zoom").value
    except ObjectDoesNotExist:
        zoom = 11
    return {"problem": problem, "zoom": zoom,
            "is_can_edit": problem.is_can_edit(request.user),
            "is_followed": problem.follow_by.filter(id=request.user.id).exists()}


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
        problem = form.save()
        if problem.status == "creating":
            Comment.add_root(fk_item=problem, created_when=now(), created_by=None, content=None)
            problem.status = "published"
            problem.save()
        messages.success(request, _("Changes saved"))
        return HttpResponseRedirect(reverse("site_problem_view", args=(problem.id,)))
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


def process_follow(request):
    if request.method != 'POST':
        return HttpResponse("Use post")
    problem = get_object_or_404(Problem, id=request.POST.get("id"))
    if problem.follow_by.filter(id=request.user.id).exists():
        problem.follow_by.remove(request.user)
        message = _("You sucessfully unsubscribe from this problem")
    else:
        problem.follow_by.add(request.user)
        message = _("You sucessfully subscribe to this problem")
    messages.success(request, message)
    return HttpResponseRedirect(problem.get_absolute_url())