from django import forms
from tags.models import Tags


class CreateTagForm(forms.ModelForm):
    tag = forms.CharField(max_length=20)
    description = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Tags
        exclude = ['slug', 'number']
        fields = ['tag', 'description']



