from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Selection(models.Model):
    """
    Represents a Selection containing Movies and Users that can vote on these Users
    """
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name="selections_owned")
    users = models.ManyToManyField('auth.User', through="UserInSelection")
    in_round = models.IntegerField(default=0)
    max_movies_per_user = models.IntegerField(default=3)
    has_winner = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)


class UserInSelection(models.Model):
    """
    Represents the relation of a user being part of a Selection
    """
    user = models.ForeignKey('auth.User', related_name="selections")
    selection = models.ForeignKey(Selection)
    # TODO: change to False when other is implemented
    accepted = models.BooleanField(default=True)


class MovieInSelection(models.Model):
    """
    Represents the relation of a movie being in a Selection
    """
    movie_id = models.IntegerField()
    selection = models.ForeignKey(Selection, related_name="movies")
    is_eliminated = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User')


class Vote(models.Model):
    """
    Represents a vote casted by a user for a movie in a selection
    """
    created = models.DateTimeField(auto_now_add=True)
    voting_round = models.IntegerField()
    is_upvote = models.BooleanField(default=False)
    movie_in_selection = models.ForeignKey(MovieInSelection)
    selection = models.ForeignKey(Selection, related_name="votes")
    voter = models.ForeignKey('auth.User')


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Make sure every User has a Token generated on registering
    """
    if created:
        Token.objects.create(user=instance)
