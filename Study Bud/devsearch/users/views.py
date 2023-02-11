from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile, Skill

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

    if request.user.is_authenticated:
        return redirect ('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print("Username dose not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            print("User or Password dose not exist.")

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    return redirect('login')