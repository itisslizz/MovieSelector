# -*- coding: utf-8 -*-
from rest_framework import serializers
from movieselector.models import Movie, Selection
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ('movie_id', 'imdb_id')

class SelectionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Selection
    fields = ('id','owner','users')

class UserSerializer(serializers.ModelSerializer):
    selections = serializers.PrimaryKeyRelatedField(many=True, queryset=Selection.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'selections')
