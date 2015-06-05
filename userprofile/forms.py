from django import forms
from userprofile.models import UserProfile
from django.contrib.auth.models import User


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


class UserDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'date_joined']
        fields = ['first_name', 'last_name']


# class EditProfileForm(forms.ModelForm):
