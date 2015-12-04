from django.db import models


class Selection(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey('auth.User', related_name="selections_owned")
  users = models.ManyToManyField('auth.User', related_name="selections")
  in_round = models.IntegerField(default=0)
  max_movies_per_user = models.IntegerField(default=3)
  has_winner = models.BooleanField(default=False)

  class Meta:
      ordering = ('created',)

class MovieInSelection(models.Model):
  movie_id = models.IntegerField()
  selection = models.ForeignKey(Selection, related_name="movies")
  is_eliminated = models.BooleanField(default=False)
  owner = models.ForeignKey('auth.User')

class Vote(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  voting_round = models.IntegerField()
  is_upvote = models.BooleanField(default=False)
  movie_in_selection = models.ForeignKey(MovieInSelection)
  voter = models.ForeignKey('auth.User')
