from django import forms
from workplaceprofile.models import *
from userprofile.models import UserProfile


class SetSkillsForm(forms.ModelForm):
    skills = forms.CharField(max_length=255)

    class Meta:
        model = UserProfile
        exclude = ['primary_workplace', 'user', 'gender', 'job_position', 'point', 'profile_image', 'experience']
        fields = ['skills']


class EditProfileForm(forms.ModelForm):

    GenderChoices = (('M', 'Male'), ('F', 'Female'),)
    gender = forms.ChoiceField(choices=GenderChoices, required=True)

    experience = forms.CharField(max_length=5000)

    class Meta:
        model = UserProfile
        exclude = ['user', 'profile_image', 'interests', 'area', 'approved', 'primary_workplace', 'job_position', 'points']




# class EditProfileForm(forms.ModelForm):
