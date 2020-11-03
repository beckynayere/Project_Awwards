from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Rate)
admin.site.register(models.Project)

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Post, Profile, Rate,Project
# from pyuploadcare.dj.forms import ImageField


# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


# class PostForm(forms.ModelForm):
#     photo = ImageField(label='')

#     class Meta:
#         model = Post
#         fields = ('photo', 'title', 'url', 'description', 'technologies',)


# class UpdateUserForm(forms.ModelForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

#     class Meta:
#         model = User
#         fields = ('username', 'email')


# class UpdateUserProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'location', 'profile_picture', 'bio', 'contact']


# class RateForm(forms.ModelForm):
#     class Meta:
#         model = Rate
#         fields = ['design', 'usability', 'content']