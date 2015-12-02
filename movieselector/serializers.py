# -*- coding: utf-8 -*-
from rest_framework import serializers
from movieselector.models import Movie, Selection, MovieInSelection, Vote
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ('movie_id', 'imdb_id')


class MovieInSelectionSerializer(serializers.ModelSerializer):
    movie = serializers.ReadOnlyField(source='movie.movie_id')
    selection = serializers.ReadOnlyField(source='selection.id')
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Round
        fields = ('id', 'movie', 'selection','owner')


class UserSerializer(serializers.ModelSerializer):
    selections_owned = serializers.PrimaryKeyRelatedField(many=True, queryset=Selection.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'selections_owned')


class SelectionSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')
  users = UserSerializer(many=True)

  class Meta:
    model = Selection
    fields = ('id','owner','users','created')


class VoteSerializer(serializers.ModelSerializer):
    selection = serializers.ReadOnlyField(source='selection.id')
    movie_in_selection = serializers.ReadOnlyField(source='movie_in_selection.id')
    voter = serializers.ReadOnlyField(source='voter.username')
    class Meta:
        model = Round
        fields = ('id','selection','is_upvote','movie_in_selection','voter')
