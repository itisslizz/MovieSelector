# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.IntegerField(serialize=False, primary_key=True)),
                ('imdb_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MovieInSelection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_eliminated', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(to='movieselector.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('in_round', models.IntegerField(default=0)),
                ('max_movies_per_user', models.IntegerField(default=3)),
                ('has_winner', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(related_name='selections_owned', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='selections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('voting_round', models.IntegerField()),
                ('is_upvote', models.BooleanField(default=False)),
                ('movie_in_selection', models.ForeignKey(to='movieselector.MovieInSelection')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='movieinselection',
            name='selection',
            field=models.ForeignKey(related_name='movies', to='movieselector.Selection'),
        ),
    ]
