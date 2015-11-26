from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
  movie_id = models.IntegerField(primary_key=True)
  imdb_id = models.CharField(max_length=10)

class Selection(models.Model):
  owner = models.ForeignKey(User, related_name="selections_owned")
  users = models.ManyToManyField(User, related_name="selections")
  max_movies_per_user = models.IntegerField(default=3)
  has_winner = models.BooleanField(default=False)

class MovieInSelection(models.Model):
  movie = models.ForeignKey(Movie)
  selection = models.ForeignKey(Selection, related_name="movies")
  is_eliminated = models.BooleanField(default=False)

class Round(models.Model):
  selection = models.ForeignKey(Selection, related_name="rounds")
  number = models.IntegerField()
  is_closed = models.BooleanField(default=False)

class Vote(models.Model):
  voting_round = models.ForeignKey(Round, related_name="votes")
  is_upvote = models.BooleanField(default=False)
  movie_in_selection = models.ForeignKey(MovieInSelection)
  voter = models.ForeignKey(User)
