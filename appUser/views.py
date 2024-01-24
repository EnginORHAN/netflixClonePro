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
    
    if request.method == "POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
    
        if fname and lname and username and email and password1:
            if password1==password2:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        up_bool=False
                        num_bol=False                 
                        # Password Control
                        for i in password1:
                            if i.isnumeric():
                                num_bol=True
                            if i.isupper():
                                up_bool=True
                            if len(password1) >=8 and num_bol and up_bool:
                            #Kayıt edilebilir
                                user= User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password1)
                                user.save()
                                return redirect('loginPage')
    context={}
    return render(request,"user/register.html",context)