#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from annoying.decorators import render_to, ajax_request

from cityproblems.site.models import Problem
from .models import Comment
from .utils import *

import json

User = get_user_model()

FK_Item = Problem


def prepareComments(comments):
    User = get_user_model()
    for j in comments:
        i = j["data"]
        authorID = i.pop("created_by")
        user = User.objects.only("username").get(id=authorID)
        i["username"] = user.username
        i["avatar"] = user.get_avatar()
        i.pop("fk_item")
        if "children" in j and j["children"]:
            j["children"] = prepareComments(j["children"])
    return comments


get = lambda id: Comment.objects.get(pk=id)


@ajax_request
def getCommentsLstJSON(request, fk_item_id):
    if not request.user.is_authenticated():
        return {"Error": _("Login please")}
    try:
        fk_item = FK_Item.objects.get(id=fk_item_id)
    except ObjectDoesNotExist:
        return {"Error": "No such topic"}
    root = Comment.objects.filter(fk_item=fk_item)[:1]
    if root:
        root = root[0].get_root()
        comments = Comment.dump_bulk(root)
        if "children" in comments[0] and comments[0]["children"]:
            comments = comments[0]["children"]
            comments = prepareComments(comments)
        else:
            comments = list()
        return {"Comments": comments}
    else:
        return {"Comments": []}


@ajax_request
def saveCommentJSON(request, fk_item_id):
    if not request.user.is_authenticated():
        return {"Error": _("Login please")}
    try:
        body = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return {'Error': "Error: can`t parse message"}
    if not ('parentID' in body and "text" in body and body['text']):
        return {'Error': "Error: Empty message"}
    if len(body['text']) > 10000:
        return {'Error': _("Error: Message too long.")}
    try:
        fk_item = FK_Item.objects.get(id=fk_item_id)
    except ObjectDoesNotExist:
        return {'Error': "Page not exists"}
    try:
        if body['parentID'] == '0':
            root = Comment.objects.filter(fk_item=fk_item)[:1][0].get_root()
            sendReplyNotification = False
        else:
            root = get(body['parentID'])
            sendReplyNotification = True
    except ObjectDoesNotExist:
        return {'Error': _("Error: Parent not found. Try reload page.")}
    comment = root.add_child(fk_item=fk_item, created_when=now(), created_by=request.user, content=escape(body['text']))
    if sendReplyNotification and root.created_by != comment.created_by:
        send_comment_reply_notification(request, root, comment)
    send_forum_item_follow_notification(request, comment)
    return dict(id=comment.id, avatar=request.user.get_avatar())


@ajax_request
def saveCommentChangesJSON(request):
    if not request.user.is_authenticated():
        return {"Error": _("Login please")}
    try:
        body = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return {'Error': "Error: can`t parse message"}
    if len(body['text']) > 10000:
        return {'Error': _("Error: Message too long.")}
    if not ('id' in body and "text" in body and body['text']):
        return {'Error': "Error: Empty message"}
    try:
        comment = get(body.get('id'))
    except ObjectDoesNotExist:
        return {'Error': _("Error: Comment not found. Try reload page.")}
    if request.user != comment.created_by:
        return {'Error': _("Error: Permission denied.")}
    comment.content = escape(body['text'])
    comment.save()
    return {"Result": "Ok"}


@ajax_request
def rmCommentJSON(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return {'Error': "Error: can`t parse message"}
    try:
        comment = get(body.get('id'))
    except ObjectDoesNotExist:
        return {'Error': _("Error: Comment not found. Try reload page.")}
    if not comment.have_write_permission(request.user):
        return {'Error': _("Error: Permission denied.")}
    comment.delete()
    return {"Result": "Ok"}


@render_to("comments/comment.html")
def getCommentHTML(request):
    return {}
