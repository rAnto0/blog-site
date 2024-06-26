# Generated by Django 5.0.6 on 2024-06-19 16:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='posts',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='post', to='main_app.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='posts',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='main_app.tagpost', verbose_name='Теги'),
        ),
        migrations.AddIndex(
            model_name='posts',
            index=models.Index(fields=['-time_create'], name='main_app_po_time_cr_02ac04_idx'),
        ),
    ]
