# -*- coding: utf-8 -*-
from rest_framework import serializers
from movieselector.models import Movie, Selection, MovieInSelection, Vote
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ('movie_id', 'imdb_id')


class UserSerializer(serializers.ModelSerializer):
    selections_owned = serializers.PrimaryKeyRelatedField(many=True, queryset=Selection.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'selections_owned')


class SelectionSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')
  #users = UserSerializer(many=True)

  class Meta:
    model = Selection
    fields = ('id','owner','created','max_movies_per_user','has_winner','in_round')

class MovieInSelectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    selection = serializers.SlugRelatedField(queryset=Selection.objects.all(),slug_field='id')
    class Meta:
        model = MovieInSelection
        fields = ('id', 'movie', 'selection','owner')


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source='voter.username')
    class Meta:
        model = Vote
        fields = ('id','is_upvote','voting_round','movie_in_selection','voter')
