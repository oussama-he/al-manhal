# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-30 19:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-published_date'],
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('content', models.TextField(blank=True, verbose_name='Annotation')),
                ('source', models.FileField(blank=True, upload_to=utils.utils.upload_to, verbose_name='La source')),
                ('source_url', models.URLField(blank=True, verbose_name='La source')),
                ('archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(blank=True, max_length=300, verbose_name='Sujet')),
                ('contributor', models.CharField(blank=True, max_length=300, verbose_name='Contributeur')),
                ('coverage', models.CharField(blank=True, max_length=300, verbose_name='couverture')),
                ('creator', models.CharField(blank=True, max_length=300, verbose_name='Createur')),
                ('date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=1500)),
                ('format', models.CharField(blank=True, max_length=100)),
                ('identifier', models.CharField(blank=True, max_length=100, verbose_name='Identifiant')),
                ('publisher', models.CharField(blank=True, max_length=300, verbose_name='Editeur')),
                ('relation', models.CharField(blank=True, max_length=300)),
                ('rights', models.TextField(blank=True, max_length=1500, verbose_name='Droits')),
                ('type', models.CharField(blank=True, max_length=100)),
                ('language', models.CharField(blank=True, max_length=100, verbose_name='Langue')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='Projet')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=0)),
                ('publication', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rated', to='portal.Publication')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='rating',
            field=models.ManyToManyField(related_name='rating', through='portal.Rating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publication',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='publication',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Publication'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]