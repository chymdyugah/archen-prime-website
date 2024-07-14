from django import forms

from projects.models import Images


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image', 'project']

