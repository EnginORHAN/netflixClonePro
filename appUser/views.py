from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from appUser.models import *
from django.contrib.auth.decorators import login_required # giriş yapmayan kişileri kısıtla

@login_required(login_url="loginPage")
def hesapPage(request):
    profile = Profile.objects.get(user = request.user, islogin = True)
    
    if request.method == "POST":
        submit = request.POST.get("submit")
        if submit == "emailSubmit":
            email = request.POST.get("email")
            password = request.POST.get("password")
            if request.user.check_password(password): #true yada false döndürür
                request.user.email = email
                request.user.save()
                return redirect("hesapPage")
            else:
                messages.error(request, "Şifre Yanlış email değiştirilemedi")
        elif submit == "passwordSubmit":
            password = request.POST.get("password")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if request.user.check_password(password):
                if password1 == password2:
                    request.user.set_password(password1)
                    request.user.save()
                    return redirect("loginPage")
                else:
                    messages.error(request, "Yeni şifreler birbiri ile uyuşmuyor")
            else:
                messages.error(request, " şifreniz yanlış şifre değiştirilemedi")
        elif submit == "telSubmit":
            tel = request.POST.get("tel")
            password = request.POST.get("password")
            if request.user.check_password(password):
                request.user.userinfo.tel = tel
                request.user.userinfo.save()
                return redirect("hesapPage")
            else:
                messages.error(request, "Şifreniz yanlış Telefon değiştiirlemedi")       
    context={
        "profile":profile,
    }
    return render(request,"hesap.html",context)

@login_required(login_url="loginPage")
def profilePage(request):
    context={}
    profile_list = Profile.objects.filter(user=request.user, isview=True)
    profile_delete_list = Profile.objects.filter(user=request.user, isview=False)
    if request.method == "POST":
        submit = request.POST.get("submit")
        title = request.POST.get("title")
        image = request.FILES.get("image")

        if submit =="profileCreate":
            if len(profile_list) <4:     
                if title and image:
                    if profile_delete_list.filter(title=title).exists(): #true yada fals döndürtür exists silinen profil olup olmadığını tespit et 
                        context.update({"is_delete_title":True, "title":title, "image":image})
                        profile = Profile(title=title,image=image,user=request.user,isview=False , isnew = True)
                        profile.save()
                    else:
                        profile = Profile(title=title,image=image,user=request.user)
                        profile.save()
                        return redirect("profilePage")
                else:
                    messages.warning(request,"boş bırakılan yerler var")
        elif submit == "newProfileCreate":
            profiledelete = profile_delete_list.get(title = title, isnew=False) #aynı isme sahip eski profil
            profiledelete.delete()
            profile = Profile.objects.get(user = request.user, isnew=True) #yeni oluşturduğumuz profili getir
            profile.isnew=False
            profile.isview=True
            profile.save()
            return redirect("profilePage")
        
        elif submit == "oldProfileCreate":
            profile = Profile.objects.get(title = title, isnew=True)
            profile.delete()
            profiledelete = profile_delete_list.get(title = title, isnew=False)
            profiledelete.isview = True
            profiledelete.save()
            return redirect("profilePage")
        
        elif submit == "profileUpdate":
            
            profileid = request.POST.get("profileid") 
            profile = Profile.objects.get(user = request.user, id=profileid)
            if title:
                profile.title = title 
            if image:
                profile.image = image 
            profile.save()
            return redirect("profilePage")
            
        
    context.update({
        "profile_list":profile_list,
    })
    return render(request,"profile.html",context)

@login_required(login_url="loginPage")
def profileDelete(request,pid):
    profile = Profile.objects.get(user=request.user,id=pid)
    profile.isview = False
    profile.save() 
    return redirect("profilePage")

@login_required(login_url="loginPage")
def profileLogin(request,pid):
    
    profile_list = Profile.objects.filter(user = request.user) # kullanıcının tüm profilleri
    profile_list.update(islogin=False) #listedeki tüm isloginleri false yapar
    
    profile = Profile.objects.get(user = request.user, id=pid) #tıklanan profil
    profile.islogin = True # giriş li olan profil
    profile.save() # kaydet
    return redirect("browseindexPage")

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
    
@login_required(login_url="loginPage")
def logoutUser(request):
    logout(request)
    return redirect("loginPage")