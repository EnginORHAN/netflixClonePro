from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Userinfo(models.Model):
    user = models.OneToOneField(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    tel = models.CharField(("Telefon"), max_length=50, default="-", blank=True)

    def __str__(self) -> str:
        return self.user.username


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    title = models.CharField(("Başlık"), max_length=50)
    image= models.ImageField(("Profil resmi"), upload_to="profile", max_length=250)
    isview = models.BooleanField(("Görüntüle"),default=True)
    isnew = models.BooleanField(("Silinen yeni profilmi"), default = False) #yeni profil olup olmadığını anlıcaz
    islogin = models.BooleanField(("Girişli profil"), default= False)
    
    def __str__(self) -> str:
        return self.title