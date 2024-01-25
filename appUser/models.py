from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    title = models.CharField(("Başlık"), max_length=50)
    image= models.ImageField(("Profil resmi"), upload_to="profile", max_length=250)
    
    def __str__(self) -> str:
        return self.title