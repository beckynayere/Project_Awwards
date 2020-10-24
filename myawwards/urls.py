from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


]