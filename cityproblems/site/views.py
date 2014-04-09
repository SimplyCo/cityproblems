#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import base64

from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
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
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import *
from .forms import *
from .utils import *
from cityproblems.admin.models import SiteParameters
from cityproblems.comments.models import Comment

from annoying.decorators import render_to, ajax_request

User = get_user_model()


@render_to('site/index.html')
def home(request):
    form = AuthenticationForm()
    return {
        'form': form,
        "center": get_map_center()
    }


@render_to('site/no_permissions.html')
def no_permissions(request):
    return {}


class UserDashboard(ListView):
    model = Problem
    paginate_by = settings.PROBLEMS_OBJECTS_PER_PAGE
    context_object_name = "problems"
    template_name = "site/site_user_dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDashboard, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get("reportBy") == "me":
            problems = self.request.user.problem_set.all()
        else:
            problems = Problem.objects.all()
        self.statuses = Problem.get_admin_statuses(in_base64=False)
        self.statuses.insert(0, ("all", _("All")))
        statuses = list()
        self.status = None
        status = self.kwargs.get("status")
        for i in self.statuses:
            if i[0] == status:
                self.status = i[1]
            statuses.append(i[0])
        if status not in statuses:
            raise Http404
        if not status == "all":
            problems = problems.filter(status=status)
        category_id = int(self.kwargs.get("category"))
        if not category_id:
            return problems.exclude(status="creating")
        category = get_object_or_404(ProblemCategory, id=category_id)
        problems = problems.filter(category=category)
        self.category = category.title
        return problems.exclude(status="creating")

    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)
        context["currentPage"] = self.kwargs.get("reportBy")
        context["status"] = dict(title=self.status, status=self.kwargs.get("status"))
        context["statuses"] = self.statuses
        categories = list(ProblemCategory.objects.all().values("id", "title"))
        categories.insert(0, dict(id=0, title=_("All")))
        context["category"] = dict(title=self.category if int(self.kwargs.get("category")) else _("All"), category=self.kwargs.get("category"))
        context["categories"] = categories
        return context


@login_required
@render_to('site/site_problem_view.html')
def problem_view(request, id=None):
    if id is None:
        raise Http404
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
            problem.status = "open"
            problem.save()
        messages.success(request, _("Changes saved"))
        return HttpResponseRedirect(reverse("site_problem_view", args=(problem.id,)))
    files = base64.standard_b64encode(json.dumps(problem.get_images()))
    return {"form": form, "center": get_map_center(), "problem": problem, "files": files}


@login_required
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


@ajax_request
def process_problem_status_change(request, obj_id):
    if not request.user.is_authenticated():
        return {"Error": _("Login please")}
    try:
        body = json.loads(request.body)
    except ValueError:
        return {'Error': "Error: can`t parse message"}
    problem = get_object_or_404(Problem, id=obj_id)
    if not problem.is_can_edit(request.user):
        return {'Error': _("Error: Permission denied.")}
    if request.user.is_staff:
        tmpStatuses = problem.get_admin_statuses(in_base64=False)
    else:
        tmpStatuses = problem.get_statuses(in_base64=False)
    statuses = list()
    for i in tmpStatuses:
        statuses.append(i[0])
    if not body.get("status") in statuses:
        return {'Error': _("Error: Wrong status.")}
    problem.status = body.get("status")
    problem.save()
    return {"success": _("Status changed successfully")}


@ajax_request
def get_main_page_markers(request):
    if not request.user.is_authenticated():
        return {"error": _("Login please")}
    if request.method != 'POST':
        return HttpResponse("Use POST")
    try:
        body = json.loads(request.body)
    except ValueError:
        return {'error': "Error: can`t parse message"}
    problems = Problem.objects.filter(status="open", longitude__gt=0, latitude__gt=0)
    if body.get("reportBy") == "me":
        problems = problems.filter(author=request.user)
    if not body.get("category") is None:
        try:
            category = ProblemCategory.objects.get(id=body.get("category"))
            problems = problems.filter(category=category)
        except ObjectDoesNotExist:
            pass
    problems = problems.values("latitude", "longitude", "title", "id")
    return {"problems": list(problems)}
