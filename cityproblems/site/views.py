#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers

from annoying.decorators import render_to


@render_to('site/index.html')
def home(request):
    return {}


@render_to('site/no_permissions.html')
def no_permissions(request):
    return {}