from rest_framework import serializers
from movieselector.models import UserInSelection


def selection_not_started(selection):
    if selection.in_round > 0:
        raise serializers.ValidationError({'message':'Selection has already started'})

def user_is_unique(users, user):
    if len(users.filter(user=user)):
        raise serializers.ValidationError({'message':'User already in selection'})

def movie_is_unique(movies, movie_id):
    if len(movies.filter(movie_id=movie_id)):
        raise serializers.ValidationError({'message':'Movie Already In Selection'})

def user_not_maxed_out(movies, user, max):
    if len(movies.filter(owner=user)) == max:
        raise serializers.ValidationError({'message':'You already reached your max movies'})


# Create Votes
def round_is_valid(selection, voting_round):
    # Can we already vote?
    voting_round = int(voting_round)
    if voting_round == 0:
        raise serializers.ValidationError({'message':'Round 0 does not accept votes'})
    # Is the vote for the active round?
    if selection.in_round != voting_round:
        raise serializers.ValidationError({'message':'Can only vote in active round'})

def not_yet_voted(votes):
    if votes:
        raise serializers.ValidationError({'message':'You can only vote once per movie per round'})
