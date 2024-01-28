from django.shortcuts import render
from appUser.models import Profile
from appMy.models import *
from django.contrib.auth.decorators import login_required

def indexPage(request):
    context={}
    return render(request,"index.html",context)

@login_required(login_url="loginPage")
def browseindexPage(request,slug=None):
    profile = Profile.objects.get(user = request.user, islogin = True)

    context={
        "profile":profile,
    }
    return render(request,"browse-index.html",context)

def netflix(request,slug=None):
    profile = Profile.objects.get(user = request.user, islogin = True)
    context={
        "profile":profile,
    }
    if slug=="yenivepopuler":
        movie = Movie.objects.filter(isnew=True).order_by("-id")
        context.update({
            "movie":movie
        })
    elif slug=="filmler" or "diziler":
        movie = Movie.objects.filter(category__title=slug).order_by("-id")
        context.update({
            "movie":movie
        })
    return render(request,"category.html",context)