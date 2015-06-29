from django import forms
from workplace.models import Workplace
from tags.models import Tags
from userprofile.models import UserProfile


class WorkplaceForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'Enter the name of your Enterprise/Group'}))
    Workplace_Type = (
        ('A', 'Large Scale Industry'),
        ('B', 'Small & Medium Scale Enterprise'),
        ('C', 'SAE Collegiate Club'),
        ('O', 'Educational Institution')
    )
    workplace_type = forms.ChoiceField(choices=Workplace_Type, widget=forms.RadioSelect(attrs={'class': 'regDropDown'}))

    class Meta:
        model = Workplace
        exclude = ['segments', 'verified', 'slug', 'materials']
        fields = ['name', 'workplace_type']


class SetWorkplaceForm(forms.ModelForm):
    workplace = forms.CharField(widget=forms.TextInput(attrs={'class':'taggable', 'data-search':'workplace', 'data-results':'single', 'data-create':'create_new', 'autocomplete':"off", 'placeholder':'Search for your Company, Team or Institution ...'}), required=True, max_length=255)

    job_position = forms.CharField(max_length=255)

    class Meta:
        model = UserProfile
        exclude = ['user', 'gender', 'points', 'experience', 'image', 'image_thumbnail', 'primary_workplace']
        fields = ['workplace', 'job_position']


class SetTeamTypeForm(forms.ModelForm):
    segments = forms.ModelMultipleChoiceField(queryset=Tags.objects.filter(type='S'))

    class Meta:
        model = Workplace
        exclude = ['name', 'workplace_type', 'materials', 'slug', 'verified']
        fields = ['segments']


class SetSegmentForm(forms.ModelForm):
    segments = forms.ModelMultipleChoiceField(queryset=Tags.objects.exclude(type='C'))

    class Meta:
        model = Workplace
        exclude = ['name', 'workplace_type', 'materials', 'slug', 'verified']
        fields = ['segments']


class EditTeamForm(forms.ModelForm):
    city = forms.CharField(max_length=50, required=False)          ## later change it to queryset
    address = forms.CharField(max_length=255, required=False)
    contact = forms.CharField(max_length=255, required=False)
    about = forms.CharField(widget=forms.Textarea, max_length=5000, required=False)
    institution_name = forms.CharField(max_length=50, required=False)        ## later change it to queryset
    participation = forms.CharField(max_length=255, required=False)
    logo = forms.ImageField(required=False)

    # def dude

    class Meta:
        model = Workplace
        exclude = ['workplace', 'points', 'materials', 'area', 'institution', '']
        fields = ['city', 'institution_name', 'address', 'contact', 'about', 'participation']





