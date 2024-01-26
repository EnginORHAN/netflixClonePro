from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from appMy.views import *
from appUser.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", indexPage,name="indexPage"),
    path("netflix", browseindexPage,name="browseindexPage"),
    path("hesap", hesapPage,name="hesapPage"),
    path("profile", profilePage,name="profilePage"),
    path("profileDelete/<pid>", profileDelete,name="profileDelete"),
    path("profileLogin/<pid>", profileLogin,name="profileLogin"),
    path("logoutUser", logoutUser,name="logoutUser"),
    
    
    path("login", loginPage,name="loginPage"),
    path("signup", registerPage,name="registerPage"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
