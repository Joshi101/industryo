from django import forms
from forum.models import Question


class AskForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea, max_length=5000, required=False)
    title = forms.CharField(widget=forms.Textarea, max_length=255, required=False)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
                           max_length=255,
                           required=False,
                           help_text='Use spaces to separate the tags, such as "asp.net mvc5 javascript"')

    class Meta:
        model = Question
        exclude = ['user', 'slug', 'vote', 'time', 'answered', 'image', 'admin_score']
        fields = ['question', 'title', 'tags']





