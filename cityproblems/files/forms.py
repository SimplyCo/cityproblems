from django import forms


class ImageValidationForm(forms.Form):
    file = forms.ImageField()
