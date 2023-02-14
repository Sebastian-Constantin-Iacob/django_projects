from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile, Skill
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreatrionForm, ProfileForm

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context={'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description = '')
    context = {'profile': profile, 'top_skills': top_skills, 'other_skills': other_skills}
    return render(request, 'users/user-profile.html', context)


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect ('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username dose not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "User or Password dose not exist.")

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, "User was successfully logged out!")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreatrionForm()

    if request.method == 'POST':
        form = CustomUserCreatrionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have succesfully registered!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error  has occurred during registration.')

    context={'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills,'projects': projects }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    form = ProfileForm()
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)