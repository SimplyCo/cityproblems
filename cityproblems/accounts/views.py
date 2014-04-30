#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils.translation import ugettext as _
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.forms import SetPasswordForm

from annoying.decorators import render_to

from .forms import *
from .utils import *
from .models import UserComfirmToken
from cityproblems.utils import *
from cityproblems.mailsender.mail import send_template_mail

User = get_user_model()


@render_to('accounts_form.html')
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(nextPage(request.GET, reverse("accounts_profile_view")))
    form = RegisterUserForm(request.POST or None)
    if form.is_valid():
        formData = form.cleaned_data
        form.save()
        user = auth.authenticate(username=formData['username'],
                                 password=formData['passwd2'])
        auth.login(request, user)
        accounts_send_email_confirm_link(request)
        notify_admins_new_user(request, user)
        return HttpResponseRedirect(nextPage(request.GET, reverse("home")))
    return {"form": form, "buttonTxt": _("Register"), "title": _("Register")}


@login_required
@render_to('accounts_profile.html')
def accounts_profile_view(request, username=None):
    if username is None:
        usr = request.user
    else:
        usr = get_object_or_404(User, username=username)
    return {"usr": usr}


@login_required
@render_to('accounts_profile_edit.html')
def accounts_profile_edit(request):
    form = modelform_factory(User, fields=("email", "username", "last_name", "first_name", "about_me", "avatar",))(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, _("Changes saved"))
        return HttpResponseRedirect(reverse("accounts_profile_view"))
    return {"form": form, "buttonTxt": _("Save")}


@login_required
def accounts_send_email_confirm_link(request):
    if request.user.is_valid_email:
        messages.info(request, _("Email already confirmed"))
        return HttpResponseRedirect(reverse("accounts_profile_view"))
    send_confirm_email(request, request.user, "confirm")
    messages.info(request, _("Please confirm your e-mail"))
    return HttpResponseRedirect(nextPage(request.GET, reverse("accounts_profile_view")))


@render_to('accounts_form.html')
def accounts_send_passwd_reset_link(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(nextPage(request.GET, reverse("accounts_profile_view")))
    form = RequestResetPasswdForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(email=form.cleaned_data["email"])
        send_confirm_email(request, user, "reset")
        messages.info(request, _("We send you email to reset your password"))
        return HttpResponseRedirect(nextPage(request.GET, reverse("login")))
    return {"title": _("Password reset"), "buttonTxt": _("Send"), "form": form}


@login_required
@render_to('accounts_form.html')
def accounts_passwd_change(request):
    form = ChangePasswdForm(request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, _("Password changed successful"))
        return HttpResponseRedirect(nextPage(request.GET, reverse("accounts_profile_view")))
    return {"title": _("Password change"), "buttonTxt": _("Change"), "form": form}


@render_to('accounts_form.html')
def accounts_passwd_reset(request, token):
    try:
        tokenObj = UserComfirmToken.objects.get(token=token, reason="reset", date__gt=now()-timedelta(days=settings.CONFIRM_LINK_VALID_DAYS))
    except ObjectDoesNotExist:
        messages.error(request, _("Wrong or expired link. Please request a new one."))
        return HttpResponseRedirect(nextPage(request.GET, reverse("home")))
    if request.user.is_authenticated():
        tokenObj.delete()
        return HttpResponseRedirect(nextPage(request.GET, reverse("accounts_passwd_change")))
    form = SetPasswordForm(tokenObj.user, request.POST or None)
    if form.is_valid():
        form.save()
        tokenObj.delete()
        messages.success(request, _("Password reset successful. You can login with new password"))
        return HttpResponseRedirect(nextPage(request.GET, reverse("login")))
    return {"title": _("Password reset"), "buttonTxt": _("Reset"), "form": form}


def accounts_process_email_confirm(request, token):
    UserComfirmToken.objects.filter(date__lt=now()-timedelta(days=settings.CONFIRM_LINK_VALID_DAYS)).delete()
    try:
        tokenObj = UserComfirmToken.objects.get(token=token, reason="confirm", date__gt=now()-timedelta(days=settings.CONFIRM_LINK_VALID_DAYS))
    except ObjectDoesNotExist:
        messages.error(request, _("Wrong or expired link. Please request a new one."))
        return HttpResponseRedirect(nextPage(request.GET, reverse("home")))
    tokenObj.user.is_valid_email = True
    tokenObj.user.save()
    messages.success(request, _("Thank you for email confirmation"))
    tokenObj.delete()
    return HttpResponseRedirect(nextPage(request.GET, reverse("home")))
