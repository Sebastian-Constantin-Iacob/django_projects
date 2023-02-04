from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.



def proejcts(request):
    return render(request, 'projects.html')


def project(request, pk):
    return render(request, 'single-project.html')
    