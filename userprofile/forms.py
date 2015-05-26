from django import forms
from workplaceprofile.models import *
from userprofile.models import UserProfile


class SetSkillsForm(forms.ModelForm):
    skills = forms.CharField(max_length=255)

    class Meta:
        model = UserProfile
        exclude = ['primary_workplace', 'user', 'gender', 'job_position', 'point', 'profile_image', 'experience']
        fields = ['skills']