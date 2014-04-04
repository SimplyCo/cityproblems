from django import forms
from django.utils.translation import ugettext as _

from .models import *


class ProblemEditForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ("category", "title", "location_details", "description", "latitude", "longitude")
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
