from django import forms

from scan.models import Uploads


class UploadForm(forms.ModelForm):
    class Meta:
        model = Uploads
        exclude = ['user', ]
