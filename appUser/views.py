from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

def hesapPage(request):
    context={}
    return render(request,"hesap.html",context)

def profilePage(request):
    context={}
    return render(request,"profile.html",context)

def loginPage(request):
    
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user= authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect("profilePage")
    
    context={}
    return render(request,"user/login.html",context)

def registerPage(request):
    context={}
    return render(request,"user/register.html",context)