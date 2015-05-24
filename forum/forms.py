from django import forms
from forum.models import Question


class AskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput, max_length=255, required=False)
    question = forms.CharField(widget=forms.Textarea, max_length=5000, required=False)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'taggable', 'data-search':'tag',
      'data-results':'multiple', 'data-create':'create', 'autocomplete':"off"}),
                           max_length=255,
                           required=False,
                           help_text='Use , (comma) to separate the tags, such as "asp.net,mvc5,javascript"')

    class Meta:
        model = Question
        exclude = ['user', 'slug', 'vote', 'time', 'answered', 'image', 'admin_score']
        fields = ['title', 'question', 'tags']