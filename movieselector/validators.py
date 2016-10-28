from rest_framework import serializers
from movieselector.models import UserInSelection, Vote, MovieInSelection, Selection

def not_yet_done(Selection):
    if getattr(selection, 'has_winner'):
        raise serializers.ValidationError(
            {'message': 'This selection has been completed already'}
        )

def new_max_movies_not_surpassed(new_max, selection_id):
    max_movie = 0
    for user in UserInSelection.objects.filter(selection__id=selection_id):
        max_movie = max(max_movie, MovieInSelection.objects.filter(owner=user.user).count())
    if max_movie > new_max or new_max < 1:
        raise serializers.ValidationError(
            {'message': 'New maximum already surpassed'}
        )

def only_one_movie_not_eliminated(selection_id):
    active_movies = MovieInSelection.objects.filter(selection__id=selection_id).\
        filter(is_eliminated=False)
    if active_movies.count() > 1:
        raise serializers.ValidationError(
            {'message': 'Selection does not have winner yet'}
        )


def is_one_increment(new, old):
    if not (new - 1 == old):
        raise serializers.ValidationError(
            {'message': 'Can only go to very next round'}
        )


def selection_not_started(selection):
    if selection.in_round > 0:
        raise serializers.ValidationError(
            {'message': 'Selection has already started'}
        )


def user_is_unique(users, user):
    if users.filter(user=user).count():
        raise serializers.ValidationError(
            {'message': 'User already in selection'}
        )

# Movie Creation


def movie_is_unique(movies, movie_id):
    if movies.filter(movie_id=movie_id).count():
        raise serializers.ValidationError(
            {'message': 'Movie Already In Selection'}
        )


def user_not_maxed_out(movies, user, max):
    if movies.filter(owner=user).count() == max:
        raise serializers.ValidationError(
            {'message': 'You already reached your max movies'}
        )

# Movie Update


def is_unchanged(old, new):
    if not (old == new):
        raise serializers.ValidationError(
            {'message': 'Forbidden changes in update'}
        )


def eliminated_to_false(old, new):
    if old:
        raise serializers.ValidationError(
            {'message': 'Movie has already been eliminated'}
        )
    if not new:
        raise serializers.ValidationError({'message': 'No update detected'})


def voting_round_complete(selection_id):
    selection = Selection.objects.get(id=selection_id)
    votes = len(Vote.objects.filter(selection__id=selection_id).
                filter(voting_round=getattr(selection, 'in_round')))
    users = getattr(selection, 'users').count()
    movies = MovieInSelection.objects.filter(selection__id=selection_id).\
        filter(is_eliminated=False).count()
    if not votes == users * movies:
        raise serializers.ValidationError(
            {'message': 'The voting round has not been completed no update allowed'}
        )


def has_been_eliminated(movie_update, voting_round):
    myvotes = Vote.objects.filter(movie_in_selection__id=movie_update['id']).\
        filter(voting_round=voting_round).\
        filter(is_upvote=True).count()
    max_votes = 0
    for movie in MovieInSelection.objects.\
            filter(selection__id=movie_update['selection_id']).\
            filter(is_eliminated=False):
        upvotes = Vote.objects.filter(movie_in_selection__id=movie_update['id']).\
            filter(voting_round=voting_round).\
            filter(is_upvote=True)
        max_votes = max(upvotes.count(), max_votes)
    if max_votes > myvotes:
        raise serializers.ValidationError(
            {'message': 'Movie has (co-)most votes cannot be eliminated'}
        )

# Create Votes


def round_is_valid(selection, voting_round):
    # Can we already vote?
    voting_round = int(voting_round)
    if voting_round == 0:
        raise serializers.ValidationError(
            {'message': 'Round 0 does not accept votes'}
        )
    # Is the vote for the active round?
    if selection.in_round != voting_round:
        raise serializers.ValidationError(
            {'message': 'Can only vote in active round'}
        )


def has_multiple_movies(selection_id):
    active_movies = MovieInSelection.objects.filter(selection__id=selection_id).\
        filter(is_eliminated=False)
    if active_movies < 2:
        raise serializers.ValidationError(
            {'message': 'Selection has a winner'}
        )


def not_yet_voted(votes):
    if votes:
        raise serializers.ValidationError(
            {'message': 'You can only vote once per movie per round'}
        )
