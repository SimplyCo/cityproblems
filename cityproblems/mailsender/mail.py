from django.utils.translation import ugettext as _
from django.conf import settings

from .tasks import send_template_mail_async, send_template_mail_sync


def send_template_mail(to, subject=_("New message"), context={}, template="main_mail_template.html", async=True):
    template = u"{}/{}".format(settings.LANGUAGE_CODE, template)
    if async:
        send_template_mail_async(to, subject, context, template)
    else:
        send_template_mail_sync(to, subject, context, template)
