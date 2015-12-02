from django.db import models

class Movie(models.Model):
  movie_id = models.IntegerField(primary_key=True)
  imdb_id = models.CharField(max_length=10)

class Selection(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey('auth.User', related_name="selections_owned")
  users = models.ManyToManyField('auth.User', related_name="selections")
  max_movies_per_user = models.IntegerField(default=3)
  has_winner = models.BooleanField(default=False)

  class Meta:
      ordering = ('created',)

class MovieInSelection(models.Model):
  movie = models.ForeignKey(Movie)
  selection = models.ForeignKey(Selection, related_name="movies")
  is_eliminated = models.BooleanField(default=False)
  added_by = models.ForeignKey('auth.User')

class Round(models.Model):
  selection = models.ForeignKey(Selection, related_name="rounds")
  number = models.IntegerField()
  state = models.CharField(max_length=10,default="open")

class Vote(models.Model):
  voting_round = models.ForeignKey(Round, related_name="votes")
  is_upvote = models.BooleanField(default=False)
  movie_in_selection = models.ForeignKey(MovieInSelection)
  voter = models.ForeignKey('auth.User')
