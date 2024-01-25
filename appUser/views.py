from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from appUser.models import *

def hesapPage(request):
    context={}
    return render(request,"hesap.html",context)

def profilePage(request):
    
    profile_list = Profile.objects.filter(user=request.user)
    
    if request.method == "POST":
        if len(profile_list) <4:
            title = request.POST.get("title")
            image = request.FILES.get("image")
            if title and image:
                profile = Profile(title=title,image=image,user=request.user)
                profile.save()
                return redirect("profilePage")
            else:
                messages.warning(request,"boş bırakılan yerler var")
    context={
        "profile_list":profile_list,
    }
    return render(request,"profile.html",context)

def loginPage(request):
    
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        rememberme=request.POST.get("rememberme")
        
        user= authenticate(username=username,password=password)
        if user:
            login(request,user)
            
            if rememberme:
                request.session.set_expiry(604800)#1 hafta beni hatırla 
            
            return redirect("profilePage")
        else:
            messages.error(request, "Kullanıcı adı veya şifre yanlış")
            
    context={}
    return render(request,"user/login.html",context)

def registerPage(request):
    context={}
    
    if request.method == "POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        
        site = request.POST.get("check-site")
        kvkk = request.POST.get("check-kvkk")
        
        if fname and lname and username and email and password1 and site and kvkk:
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
                        else:
                            messages.error(request, "Şifreniz 8 veya daha uzun olması lazım")
                            messages.error(request, "Şifreniz en az 1 büyük harf içermeli")
                            messages.error(request, "Şifreniz en az 1 rakam içermeli")
                    else:
                        messages.error(request, "Bu email zaten kullanılıyor")
                else:
                    messages.error(request, "Kullanıcı adı daha önceden alınmış")
            else:
                messages.error(request, "Şifreler aynı değil.")
        else:
            messages.warning(request, "Boş bırakılan yerleri doldurunuz")
            context.update({"fname":fname,"lname":lname,"email":email,"username":username})

    return render(request,"user/register.html",context)

    