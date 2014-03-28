from django import forms
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

import re

User = get_user_model()


class RegisterUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.is_staff = kwargs.pop("is_staff", False)
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label='E-Mail')
        self.fields['username'] = forms.CharField(label=_("Username"), max_length=25)
        self.fields['last_name'] = forms.CharField(label=_("Last name"), max_length=25)
        self.fields['first_name'] = forms.CharField(label=_("First name"), max_length=25)
        self.fields['passwd1'] = forms.CharField(label=_("Password"),
                                               widget=forms.PasswordInput(),
                                               min_length=6, max_length=100)
        self.fields['passwd2'] = forms.CharField(label=_("Password again"),
                                               widget=forms.PasswordInput())

    def clean_passwd2(self):
        passwd1 = self.cleaned_data['passwd1']
        passwd2 = self.cleaned_data['passwd2']
        if passwd1 != passwd2:
            raise forms.ValidationError(_("Password mismatch"))
        return passwd2

    def clean_email(self):
        e_mail = self.cleaned_data['email']
        if User.objects.filter(email=e_mail).exists():
            raise forms.ValidationError(_("User with this email exists"))
        return e_mail

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("User with this username exists"))
        p = re.compile(r'^\w+$')
        if not p.search(username):
            raise forms.ValidationError(_('Wrong symbol. You can use "a-z","0-9" and "_"'))
        if len(username) > 20:
            raise forms.ValidationError(_("Username too long"))
        return username

    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'],
                                        self.cleaned_data['email'],
                                        self.cleaned_data['passwd1'])
        user.is_staff = self.is_staff
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user


class RequestResetPasswdForm(forms.Form):
    email = forms.EmailField(label=_("Input your email"))

    def clean_email(self):
        e_mail = self.cleaned_data['email']
        if not User.objects.filter(email=e_mail).exists():
            raise forms.ValidationError(_("We have no user with such e-mail"))
        return e_mail


class ChangePasswdForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop("username", None)
        super(ChangePasswdForm, self).__init__(*args, **kwargs)
        self.fields['passwd'] = forms.CharField(label=_("Old password"), widget=forms.PasswordInput(attrs={"required": ""}))
        self.fields['passwd1'] = forms.CharField(label=_("New password"), widget=forms.PasswordInput(attrs={"required": ""}))
        self.fields['passwd2'] = forms.CharField(label=_("Confirm new password"), widget=forms.PasswordInput(attrs={"required": ""}))

    def clean_passwd2(self):
        passwd1 = self.cleaned_data['passwd1']
        passwd2 = self.cleaned_data['passwd2']
        if passwd1 != passwd2:
            raise forms.ValidationError(_("Passwords don't match."))
        if len(passwd1) < 6:
            raise forms.ValidationError(_("Password too weak."))
        if len(passwd1) > 100:
            raise forms.ValidationError(_("Password too long."))
        return passwd2

    def clean_passwd(self):
        passwd = self.cleaned_data['passwd']
        self.user = auth.authenticate(username=self.username, password=passwd)
        if self.user is None:
            raise forms.ValidationError(_("Wrong password"))
        return passwd

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['passwd1'])
        if commit:
            self.user.save()
        return self.user
