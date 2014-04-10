from __future__ import absolute_import

from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from .mailsender import send_mail

from celery import shared_task

import logging

logger = logging.getLogger(__name__)


@shared_task
def send_template_mail_sync(to, subject, context, template):
    try:
        text = render_to_string(template, context)
    except Exception as e:
        logger.error(u'\n\nMessage to "{}" with subject "{}" was not sended\nTemplate: "{}" not found\n'.format(to, subject, template))
        return
    send_mail(to, subject, text, None)


def send_template_mail_async(to, subject, context, template):
    send_template_mail_sync.delay(to, subject, context, template)
