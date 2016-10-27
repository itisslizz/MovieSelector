from rest_framework import serializers
from movieselector.models import UserInSelection, Vote, MovieInSelection, Selection


def selection_not_started(selection):
    if selection.in_round > 0:
        raise serializers.ValidationError({'message':'Selection has already started'})

def user_is_unique(users, user):
    if len(users.filter(user=user)):
        raise serializers.ValidationError({'message':'User already in selection'})

# Movie Creation
def movie_is_unique(movies, movie_id):
    if len(movies.filter(movie_id=movie_id)):
        raise serializers.ValidationError({'message':'Movie Already In Selection'})

def user_not_maxed_out(movies, user, max):
    if len(movies.filter(owner=user)) == max:
        raise serializers.ValidationError({'message':'You already reached your max movies'})

# Movie Update
def only_change_is_eliminated(old, new):
    if old['movie_id'] == new['movie_id']:
        return
    else:
        raise serializers.ValidationError({'message':'Only changes to is_eliminated field are allowed'})

def eliminated_to_false(old, new):
    if old:
        raise serializers.ValidationError({'message':'Movie has already been eliminated'})
    if not new:
        raise serializers.ValidationError({'message':'No update detected'})

def voting_round_complete(selection_id):
    selection = Selection.objects.get(id=selection_id)
    votes = len(Vote.objects.filter(selection__id=selection_id).\
        filter(voting_round = getattr(selection, 'in_round')))
    users = getattr(selection,'users').count()
    movies = MovieInSelection.objects.filter(selection__id=selection_id).\
        filter(is_eliminated=False).count()
    if not votes == users*movies:
        raise serializers.ValidationError({'message':'The voting round has not been completed'})

def has_been_eliminated(movie_update, voting_round):
    myvotes = Vote.objects.filter(movie_in_selection__id=movie_update['id']).\
        filter(voting_round=voting_round).\
        filter(is_upvote=True).count()
    max_votes = 0
    for movie in MovieInSelection.objects.filter(selection__id=movie_update['selection_id']).\
        filter(is_eliminated=False):
        upvotes = Vote.objects.filter(movie_in_selection__id=movie_update['id']).\
            filter(voting_round=voting_round).\
            filter(is_upvote=True)
        max_votes = max(upvotes.count(),max_votes)
    if max_votes > myvotes:
        raise serializers.ValidationError({'message':'Movie has (co-)most votes cannot be eliminated'})

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
