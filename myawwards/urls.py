from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),


]