from django.urls import path, include,re_path
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static



router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)
router.register('profile', views.ProfileViewSet)
router.register('project', views.ProjectViewset)


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('<username>/profile', views.user_profile, name='userprofile'),
    path('profile/<username>/', views.profile, name='profile'),
    path('profile/<username>/settings', views.edit_profile, name='edit'),
    path('upload/', views.upload_project, name='upload_project'),
    path('project/<post>', views.project, name='project'),
    path('search/', views.search_project, name='search'),
    path('api/profile/', views.ProfileList.as_view()),
    re_path('rate/(?P<project_id>\d+)', views.rate_project, name='rate'),
    re_path('vote/(?P<project_id>\d+)', views.vote, name='vote'),


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
