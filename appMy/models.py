from django.db import models
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    title=models.CharField(("Kategori"), max_length=50)

    def __str__(self):
        return self.title
    
    
class Movie(models.Model):
    title = models.CharField(("Başlık"), max_length=50)
    image = models.ImageField(("Resim"), upload_to="",max_length=50)
    category = models.ForeignKey(Category, verbose_name=("Kategori"), on_delete=models.CASCADE)
    isnew=models.BooleanField(("Yenimi"))
    slug = models.SlugField(("slug"),blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self):
        self.slug = slugify(self.title)
        super().save()
    
        
