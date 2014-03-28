from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.templatetags.static import static
from django.core.urlresolvers import reverse

from uuid import uuid4


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(
            email=UserManager.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=email, password=password, username=username)
        user.is_staff = True
        user.is_superuser = True
        user.is_valid_email = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    avatar = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    about_me = models.TextField(blank=True)
    is_valid_email = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ["date_joined", "-last_login", "username"]

    def get_full_name(self):
        return u"{} {}".format(self.last_name, self.first_name)

    def get_short_name(self):
        return self.username

    def str(self):
        return self.email

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return static("img/default_avatar.png")


class UserComfirmToken(models.Model):
    REASON_CHOICES = (("confirm", "E-Mail confirm"), ("reset", "Password reset"))
    user = models.ForeignKey(User)
    token = models.CharField(max_length=50, default=str(uuid4().int))
    reason = models.CharField(choices=REASON_CHOICES, max_length=15)
    date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        if self.reason == "confirm":
            return reverse("accounts_process_email_confirm", args=(self.token,))
        return reverse("accounts_passwd_reset", args=(self.token,))
