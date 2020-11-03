from django.http  import HttpResponse, Http404,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Profile, Post, Rate, Project
from .serializer import ProfileSerializer, UserSerializer, PostSerializer, ProjectSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .forms import SignupForm,PostForm,UpdateUserForm,UpdateUserProfileForm,RateForm
import random
import datetime as dt
from .permissions import IsAdminOrReadOnly
from rest_framework import status

# Create your views here.
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()

    try:
        posts = Post.objects.all()
        posts = posts[::-1]
        a_post = random.randint(0, len(posts)-1)
        # a_post = random.randint(0, abs(len(posts)-1)), user
        random_post = posts[a_post]
        print(random_post.photo)
    except Post.DoesNotExist:
        posts = None
    return render(request, 'home.html', {'posts': posts, 'form': form, 'random_post': random_post})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ProjectViewSet(viewsets. ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='login')
def profile(request, username):
    return render(request, 'profile.html')


def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'user_profile.html', params)


@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'edit.html', params)


@login_required(login_url='login')
def project(request, post):
    post = Post.objects.get(title=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RateForm()
    params = {
        'post': post,
        'rate_form': form,
        'rate_status': rate_status

    }
    return render(request, 'project.html', params)

@login_required(login_url='/accounts/login')
def upload_project(request):
    if request.method == 'POST':
        uploadform = ProjectForm(request.POST, request.FILES)
        if uploadform.is_valid():
            upload = uploadform.save(commit=False)
            upload.profile = request.user.profile
            upload.save()
            return redirect('home_page')
    else:
        uploadform = ProjectForm()
    return render(request, 'update-project.html', locals())


def view_project(request):
    project = Project.objects.get_all()
    return render(request, 'home.html', locals())


def search_project(request):
    if request.method == 'GET':
        title = request.GET.get("title")
        results = Post.objects.filter(title__icontains=title).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'results.html', {'message': message})

def rate(request):
    profile=User.objects.get(username=request.user)
    return render(request, 'rate.html', locals())


def view_rate(request, project_id):
    user=User.objects.get(username=request.user)
    project=Project.objects.get(pk=project_id)
    rate=Rate.objects.filter(project_id=project_id)
    print(rate)
    return render(request, 'project.html', locals())


@login_required(login_url='/accounts/login')
def rate_project(request, project_id):
    project=Project.objects.get(pk=project_id)
    profile=User.objects.get(username=request.user)
    if request.method == 'POST':
        rateform=RatingsForm(request.POST, request.FILES)
        print(rateform.errors)
        if rateform.is_valid():
            rating=rateform.save(commit=False)
            rating.project=project
            rating.user=request.user
            rating.save()
            return redirect('vote', project_id)
    else:
        rateform=RatingsForm()
    return render(request, 'rate.html', locals())


class ProfileList(APIView):
    def get(self, request, format=None):
        all_profile=Profile.objects.all()
        serializers=ProfileSerializer(all_profile, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers=ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    permission_classes=(IsAdminOrReadOnly,)


class ProjectList(APIView):
    def get(self, request, format=None):
        all_project=Project.objects.all()
        serializers=ProjectSerializer(all_project, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers=ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes=(IsAdminOrReadOnly,)

@login_required(login_url='/accounts/login/')
def vote(request, project_id):
    try:
        project=Project.objects.get(pk=project_id)
        rate=Rate.objects.filter(project_id=project_id).all()
        print([r.project_id for r in rate])
        rateform=RatingsForm()
    except DoesNotExist:
        raise Http404()
    return render(request, "project.html", locals())
