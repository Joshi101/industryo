from django import forms
from workplace.models import Workplace, Segment
from userprofile.models import UserProfile


class WorkplaceForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    Workplace_Type = (
        ('A', 'Large Scale Industry'),
        ('B', 'Small & Medium Scale Enterprise'),
        ('C', 'College Teams'),
        ('O', 'Others')
    )
    workplace_type = forms.ChoiceField(choices=Workplace_Type, widget=forms.Select(attrs={'class': 'regDropDown'}))

    class Meta:
        model = Workplace
        exclude = ['segments', 'verified', 'slug', 'materials']
        fields = ['name', 'workplace_type']


class SetWorkplaceForm(forms.ModelForm):
    primary_workplace = forms.ModelChoiceField(queryset=Workplace.objects.all(), required=True)
    job_position = forms.CharField(max_length=255)

    class Meta:
        model = UserProfile
        exclude = ['user', 'gender', 'points', 'experience', 'image', 'image_thumbnail']
        fields = ['primary_workplace', 'job_position']


class SetTeamTypeForm(forms.ModelForm):
    segments = forms.ModelMultipleChoiceField(queryset=Segment.objects.filter(workplace_type='C'))

    class Meta:
        model = Workplace
        exclude = ['name', 'workplace_type', 'materials', 'slug', 'verified']
        fields = ['segments']


class SetSegmentForm(forms.ModelForm):
    segments = forms.ModelMultipleChoiceField(queryset=Segment.objects.exclude(workplace_type='C'))

    class Meta:
        model = Workplace
        exclude = ['name', 'workplace_type', 'materials', 'slug', 'verified']
        fields = ['segments']







