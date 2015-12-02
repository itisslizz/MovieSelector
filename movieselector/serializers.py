# -*- coding: utf-8 -*-
from rest_framework import serializers
from movieselector.models import Movie, Selection, Round
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
  users = UserSerializer(many=True)

  class Meta:
    model = Selection
    fields = ('id','owner','users','created')

class RoundSerializer(serializers.ModelSerializer):
    selection = serializers.ReadOnlyField(source='selection.id')
    class Meta:
        model = Round
        fields = ('id','number','state','selection')

class VoteSerializer(serializers.ModelSerializer):
    voting_round = serializers.ReadOnlyField(source='voting_round.id')
    movie_in_selection = serializers.ReadOnlyField(source='movie_in_selection.id')
    voter = serializers.ReadOnlyField(source='voter.username')
    class Meta:
        model = Round
        fields = ('id','voting_round','is_upvote','movie_in_selection','voter')
