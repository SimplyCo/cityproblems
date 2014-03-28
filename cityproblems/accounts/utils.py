from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from cityproblems.mailsender.mail import send_template_mail
from .models import UserComfirmToken

User = get_user_model()


def notify_admins_new_user(request, user):
    admins = User.objects.filter(is_staff=True)
    context = dict(new_user=user, url_to_user_profile=request.build_absolute_uri(reverse("accounts_profile_view", args=(user.username,))))
    for i in admins:
        send_template_mail(i.email, _("New user was registered"), context, "admin_on_new_user_registration.html")


def send_confirm_email(request, user, reason):
    try:
        tokenObj = UserComfirmToken.objects.get(user=user, reason=reason)
        tokenObj.date = now()
    except ObjectDoesNotExist:
        tokenObj = UserComfirmToken()
        tokenObj.user = user
        tokenObj.reason = reason
    tokenObj.save()
    if reason == "confirm":
        subject = _("Confirm your email please")
        template = "user_on_registration.html"
    else:
        subject = _("Password reset")
        template = "user_on_passwd_reset.html"
    send_template_mail(user.email, subject, {"confirm_url": request.build_absolute_uri(tokenObj.get_absolute_url()), "user": user}, template)
