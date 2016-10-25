from movieselector.models import Selection, MovieInSelection, Vote, UserInSelection
from movieselector.permissions import IsOwnerOrReadOnly, IsParticipantOrReadOnly, IsOwnerOrReadOnlyList, IsUserPutOrOwnerDeleteOnly
from movieselector.serializers import UserSerializer, UserRegisterSerializer, UserInSelectionSerializer, UserInSelectionDetailSerializer, SelectionSerializer, VoteSerializer, MovieInSelectionSerializer
from movieselector.validators import *
from rest_framework import generics, permissions, serializers
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SelectionList(generics.ListCreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SelectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # perform update
    # Only allow updates to fields if in round 0
    # Only allow updates to in_round/has_winner if in_round > 0
    # Only allow increments of 1 to in_round
    # Only allow increment to in_round if all votes have been cast (active_movies*userinselections)
    # Only allow has_winner to true if only one movie is not eliminated
    # Allow no changes after has_winner set to true



class UserInSelectionList(generics.ListCreateAPIView):
    serializer_class = UserInSelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyList,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return UserInSelection.objects.filter(selection__id=selection_id)

    def perform_create(self, serializer):
        selection_id = self.kwargs['selection_id']
        selection = Selection.objects.get(id=selection_id)
        selection_not_started(selection)
        users = UserInSelection.objects.filter(
            selection__id=selection_id);

        user_is_unique(users, serializer.validated_data['user'])
        serializer.save(selection=selection)

class UserInSelectionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInSelectionDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUserPutOrOwnerDeleteOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return UserInSelection.objects.filter(selection__id=selection_id)


class MovieInSelectionList(generics.ListCreateAPIView):
    serializer_class = MovieInSelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsParticipantOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return MovieInSelection.objects.filter(selection__id=selection_id)

    def perform_create(self, serializer):
        selection = Selection.objects.get(id=self.kwargs['selection_id'])
        selection_not_started(selection)
        movies = MovieInSelection.objects.filter(
            selection=selection)

        movie_is_unique(movies, serializer.validated_data['movie_id'])
        user_not_maxed_out(movies, self.request.user, selection.max_movies_per_user)

        serializer.save(owner=self.request.user, selection=selection)


class MovieInSelectionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieInSelectionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return MovieInSelection.objects.filter(selection__id=selection_id).all()

    #perform_update
    #  Only allow updates to is_eliminated field
    #  Only allow is_eliminated to True updates (no Backsies)
    #  Only allow updates if voting_round is complete
    #  Only allow is_eliminated to True if exists movie with more upvotes

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsParticipantOrReadOnly)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        voting_round = self.kwargs['voting_round']
        queryset = Vote.objects.filter(selection__id=selection_id).filter(voting_round=voting_round)
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            queryset = queryset.filter(movie_in_selection__id=movie_id)
        return queryset

    def perform_create(self, serializer):
        voting_round = self.kwargs['voting_round']
        selection_id = self.kwargs['selection_id']
        movie_in_selection = serializer.validated_data['movie_in_selection']
        selection = Selection.objects.get(id=selection_id)
        round_is_valid(selection, voting_round)
        votes = Vote.objects.filter(
            selection=selection,
            movie_in_selection=movie_in_selection,
            voting_round=voting_round,
            voter=self.request.user)
        not_yet_voted(len(votes))
        serializer.save(voter=self.request.user,
                        selection=selection,
                        voting_round = voting_round)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        voting_round = self.kwargs['voting_round']
        return Vote.objects.filter(selection__id=selection_id).filter(voting_round=voting_round)
