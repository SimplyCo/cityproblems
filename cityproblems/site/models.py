from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

import os

User = get_user_model()

PROBLEM_STATUS_CHOICES = (
    (u'creating', _(u'Creating')),
    (u'published', _(u'Published')),
)


class ProblemCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title


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
