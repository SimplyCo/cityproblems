from __future__ import absolute_import

from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from .mailsender import send_mail

from celery import shared_task


@shared_task
def send_template_mail_sync(to, subject, context, template):
    text = render_to_string(template, context)
    send_mail(to, subject, text, None)


def send_template_mail_async(to, subject, context, template):
    send_template_mail_sync.delay(to, subject, context, template)
