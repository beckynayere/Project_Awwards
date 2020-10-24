from rest_framework import serializers
from .models import Profile, Post
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()
    class Meta:
        model = Profile
        fields = ['name', 'profile_picture', 'bio', 'location', 'contact']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'url', 'username', 'profile', 'posts']
        # fields = ['id', 'title', 'url', 'description', 'technologies', 'photo', 'date', 'user']
