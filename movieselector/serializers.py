# -*- coding: utf-8 -*-
from rest_framework import serializers
from movieselector.models import Selection, MovieInSelection, UserInSelection, Vote
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    selections_owned = serializers.PrimaryKeyRelatedField(many=True, queryset=Selection.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'selections_owned')


class SelectionSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')
  movies = serializers.SlugRelatedField(many=True,
                                        read_only=True,
                                        slug_field='movie_id')

  class Meta:
    model = Selection
    fields = ('id','owner','created','max_movies_per_user','has_winner','in_round','movies','users')

class MovieInSelectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    selection = serializers.ReadOnlyField(source='selection.id')

    class Meta:
        model = MovieInSelection
        fields = ('id', 'movie_id', 'selection','owner','is_eliminated')

class UserInSelectionSerializer(serializers.ModelSerializer):
    selection = serializers.ReadOnlyField(source='selection.id')
    class Meta:
        model = UserInSelection
        fields = ('id', 'user', 'selection','accepted')

class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source='voter.username')
    selection = serializers.ReadOnlyField(source='selection.id')
    voting_round = serializers.ReadOnlyField()
    class Meta:
        model = Vote
        fields = ('id','is_upvote','voting_round','movie_in_selection','selection','voter')
