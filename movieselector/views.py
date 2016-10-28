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

    def perform_update(self, serializer):
        original = self.get_object()
        update = serializer.validated_data
        not_yet_done(original)
        if getattr(original, 'in_round') == 0:
            is_unchanged(getattr(original, 'has_winner'),
                         update['has_winner'])
            if (not (update['in_round'] == getattr(original,'in_round'))):
                is_one_increment(update['in_round'],
                                 getattr(original,'in_round'))
                # all_users_accepted_or_declined
            if (not (update['max_movies_per_user'] == getattr(original,
                                                              'max_movies_per_user'))):
                new_max_movies_not_surpassed(update['max_movies_per_user'],
                                             getattr(original,'id'))
        else:
            is_unchanged(getattr(original, 'max_movies_per_user'),
                         update['max_movies_per_user'])
            if (update['has_winner']):
                only_one_movie_not_eliminated(original)
                is_unchanged(getattr(original['in_round']), update['in_round'])
            elif (not (update['in_round'] == getattr(original,'in_round'))):
                is_one_increment(update['in_round'],
                                 getattr(original,'in_round'))
                voting_round_complete(getattr(original, 'id'))
        serializer.save()
    # perform update
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
            selection__id=selection_id)

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
        user_not_maxed_out(movies, self.request.user,
                           selection.max_movies_per_user)

        serializer.save(owner=self.request.user, selection=selection)


class MovieInSelectionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieInSelectionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return MovieInSelection.objects.filter(selection__id=selection_id).all()

    def perform_update(self, serializer):
        original = self.get_object().__dict__
        selection = Selection.objects.get(id=original['selection_id'])
        updated = serializer.validated_data

        is_unchanged(original['movie_id'], updated['movie_id'])
        eliminated_to_false(
            original['is_eliminated'], updated['is_eliminated'])
        voting_round_complete(original['selection_id'])
        has_been_eliminated(original, getattr(selection, 'in_round'))

        serializer.save()


class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsParticipantOrReadOnly)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        voting_round = self.kwargs['voting_round']
        queryset = Vote.objects.filter(
            selection__id=selection_id).filter(voting_round=voting_round)
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
        has_multiple_movies(selection_id)
        serializer.save(voter=self.request.user,
                        selection=selection,
                        voting_round=voting_round)


class VoteDetail(generics.RetrieveDestroyAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        voting_round = self.kwargs['voting_round']
        return Vote.objects.filter(selection__id=selection_id).filter(voting_round=voting_round)
