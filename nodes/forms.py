from django import forms
from nodes.models import Images
from tags.models import Tags


class UploadImageForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    # caption = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Images
        exclude = ['slug', 'user', 'image_thumbnail', 'time']
        fields = ['image']


class SetLogoForm(forms.ModelForm):
    image = forms.ImageField(required=True,widget=forms.FileInput(attrs={'class':'cropit-image-input'}))

    class Meta:
        model = Images
        exclude = ['slug', 'user', 'image_thumbnail', 'time']
        fields = ['image']


class SetProfileImageForm(forms.ModelForm):
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class':'cropit-image-input'}))

    class Meta:
        model = Images
        exclude = ['slug', 'user', 'image_thumbnail', 'time']
        fields = ['image']


class SetTagLogoForm(forms.ModelForm):
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class':'cropit-image-input'}))

    class Meta:
        model = Images
        exclude = ['slug', 'user', 'image_thumbnail', 'time']
        fields = ['image']


class SetProductImage(forms.ModelForm):
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'cropit-image-input'}))

    class Meta:
        model = Images
        exclude = ['slug', 'user', 'image_thumbnail', 'time']
        fields = ['image']




