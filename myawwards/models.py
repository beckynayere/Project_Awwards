from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pyuploadcare.dj.models import ImageField
import datetime as dt

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='images/', default='default.png')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(max_length=60, blank=True)
    contact = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @classmethod
    def search_user(cls, name):
        userprof = Profile.objects.filter(user__username__icontains=name)
        return userprof


class Post(models.Model):

    title = models.CharField(max_length=155)
    url = models.URLField(max_length=255)
    description = models.TextField(max_length=255)
    technologies = models.CharField(max_length=200, blank=True)
    photo = ImageField(manual_crop='1280x720')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    def delete_post(self):
        self.delete()

    @classmethod
    def search_project(cls, title):
        return cls.objects.filter(title__icontains=title).all()

    @classmethod
    def all_posts(cls):
        return cls.objects.all()

    def save_post(self):
        self.save()


class Rate(models.Model):
    design = models.CharField(max_length=30)
    usability = models.CharField(max_length=8)
    creativity = models.CharField(max_length=8, blank=True, null=True)
    average = models.FloatField(max_length=8)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='rate', null=True)

    

    def save_rate(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rate.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.post} Rate'

    class Meta:
        ordering = ['-id']

    def save_rate(self):
        self.save()

    @classmethod
    def get_rate(cls, profile):
        rate = Rate.objects.filter(Profile__pk=profile)
        return rate

    @classmethod
    def get_all_rating(cls):
        rating = Rate.objects.all()
        return rating

class Project(models.Model):

    screenshot = models.ImageField(upload_to='images/')
    project_name = models.CharField(max_length=10)
    project_url = models.CharField(max_length=50)
    location = models.CharField(max_length=10)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE , null=True, related_name='project')
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pk']

    def save_project(self):
        self.save()

    @classmethod
    def get_project(cls, profile):
        project = Project.objects.filter(Profile__pk=profile)
        return project

    @classmethod
    def get_all_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def search_by_profile(cls, search_term):
        projo = cls.objects.filter(profile__name__icontains=search_term)
        return projo

    @classmethod
    def get_profile_projects(cls, profile):
        project = Project.objects.filter(profile__pk=profile)
        return project

    @classmethod
    def find_project_id(cls, id):
        identity = Project.objects.get(pk=id)
        return identity