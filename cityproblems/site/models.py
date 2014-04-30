from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.urlresolvers import reverse

import os
import json
import base64

from .utils import get_safe_url_name

User = get_user_model()

PROBLEM_STATUS_CHOICES = (
    (u'creating', ugettext(u'Creating')),
    (u'open', ugettext(u'Open')),
    (u'closed', ugettext(u'Closed')),
    (u'rejected', ugettext(u'Rejected')),
)


class ProblemCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    url_name = models.SlugField(max_length=170, unique=True, db_index=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.url_name:
            self.url_name = get_safe_url_name(self.url_name)
        else:
            self.url_name = get_safe_url_name(self.title)
        while True:
            try:
                super(ProblemCategory, self).save(*args, **kwargs)
            except IntegrityError:
                self.url_name += "_"
            else:
                break


class Problem(models.Model):
    category = models.ForeignKey(ProblemCategory, null=True)
    author = models.ForeignKey(User)
    created_when = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300, null=True)
    location_details = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=PROBLEM_STATUS_CHOICES, default="creating")
    follow_by = models.ManyToManyField(User, related_name="follow_by")

    def is_can_edit(self, user):
        return user.is_authenticated() and (user.is_staff or user == self.author)

    def get_images(self):
        files = list()
        for i in self.problemimage_set.all():
            files.append(dict(id=i.id, thumbnail=i.thumbnail.url,
                              url=i.big_image.url, order_number=i.order_number,
                              name=i.get_name()))
        return files

    def get_absolute_url(self):
        return reverse("site_problem_view", args=(self.id,))

    @staticmethod
    def get_statuses(in_base64=True):
        statuses = [i for i in PROBLEM_STATUS_CHOICES if not(i[0] == "creating" or i[0] == "rejected")]
        if in_base64:
            return base64.standard_b64encode(json.dumps(statuses).encode("utf-8"))
        return statuses

    @staticmethod
    def get_admin_statuses(in_base64=True):
        statuses = [i for i in PROBLEM_STATUS_CHOICES if i[0] != "creating"]
        if in_base64:
            return base64.standard_b64encode(json.dumps(statuses).encode("utf-8"))
        return statuses

    def get_status(self):
        for i in PROBLEM_STATUS_CHOICES:
            if i[0] == self.status:
                return i[1]


class ProblemImage(models.Model):
    thumbnail = models.ImageField(blank=True, null=True, upload_to='images/thumbnail/%Y/%m/%d')
    small_image = models.ImageField(blank=True, null=True, upload_to='images/small_image/%Y/%m/%d')
    medium_image = models.ImageField(blank=True, null=True, upload_to='images/medium_image/%Y/%m/%d')
    big_image = models.ImageField(blank=True, null=True, upload_to='images/big_image/%Y/%m/%d')
    problem = models.ForeignKey(Problem)
    order_number = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order_number"]

    def get_name(self):
        return os.path.basename(self.big_image.name)
