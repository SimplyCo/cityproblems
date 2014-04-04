from cityproblems.mailsender.mail import send_template_mail
from django.utils.translation import ugettext as _


def send_comment_reply_notification(request, parent_comment, comment):
    context = dict(usr=parent_comment.created_by, comment=comment, fk_item_url=request.build_absolute_uri(comment.fk_item.get_absolute_url()))
    send_template_mail(parent_comment.created_by.email, _("Reply to your comment in")+u" {}".format(comment.fk_item.title), context, "user_on_comment_reply.html")


def send_forum_item_follow_notification(request, comment):
    context = dict(comment=comment, fk_item_url=request.build_absolute_uri(comment.fk_item.get_absolute_url()))
    for i in comment.fk_item.follow_by.all():
        context["usr"] = i
        send_template_mail(i.email, _("New comment in")+u" {}".format(comment.fk_item.title), context, "user_on_following_topic_comment.html")
