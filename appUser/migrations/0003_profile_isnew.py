# Generated by Django 4.2.8 on 2024-01-26 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0002_profile_isview'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='isnew',
            field=models.BooleanField(default=False, verbose_name='Silinen yeni profilmi'),
        ),
    ]
