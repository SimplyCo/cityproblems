# -*- coding: utf-8 -*-
import logging
import smtplib
try:
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Header import make_header
    from email.Utils import make_msgid as msgid
    from email.Encoders import encode_base64
except ImportError:
    # Python3 support not tested
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.header import make_header
    from email.utils import make_msgid as msgid
    from email.encoders import encode_base64
import os

from django.conf import settings

logger = logging.getLogger(__name__)
print __name__

def send_mail(to, subject, text, attach):
    ###
    if settings.DEBUG:
        logger.debug(u"\n{}\n{}\n{}\n".format(to, subject, text))
        return
    ###
    msg = MIMEMultipart('related')
    organization = settings.MAIL_SENDER_ORGANIZATION
    mailer = settings.MAIL_SENDER_MAILER
    msg['Message-ID'] = msgid()
    msg['Organization'] = make_header([(organization, 'UTF-8')])
    msg['X-Mailer'] = make_header([(mailer, 'UTF-8')])
    msg['From'] = make_header([(mailer, 'UTF-8'), ('<' + settings.MAIL_SENDER_SENDER + '>', 'us-ascii')])
    msg['To'] = make_header([(to, 'us-ascii')])
    msg['Subject'] = make_header([(subject, 'UTF-8')])
    msg.preamble = "This is a multi-part message in MIME format."
    msg.epilogue = "End of message"
    # alternative part
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msgText = MIMEText(text, '', 'utf-8')
    msgAlternative.attach(msgText)
    # html part
    to_attach = MIMEText(text.encode('utf-8'), 'html', 'utf-8')
    msgAlternative.attach(to_attach)

    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP(settings.MAIL_SENDER_SERVER, settings.MAIL_SENDER_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.MAIL_SENDER_USER, settings.MAIL_SENDER_PASSWORD)
    mailServer.sendmail(settings.MAIL_SENDER_SENDER, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
