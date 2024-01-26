from django.contrib import admin
from appUser.models import *
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

    list_display = ('user', "title","isview","id","isnew",) # görmek istediklerimiz
    list_editable = ("isview",) #içeriye girmedne değiştirilebilmesini sağlar
    # list_filter = ('',) # filtreleme verir
    # inlines = [
    #     Inline,
    # ] iki modeli birleştirmek için kullanılır
    readonly_fields = ('title',) #admin panelinden değişiklik yapılmaması için kullanıyoruz
    search_fields = ('user__username',) #admin panaline arama barı veriyor
    # date_hierarchy = '' # tarih sıralaması hirayerşisi yapar
    # ordering = ('',) #sıralama