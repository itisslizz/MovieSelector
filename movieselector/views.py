from movieselector.models import Selection, MovieInSelection, Vote, UserInSelection
from movieselector.permissions import IsOwnerOrReadOnly, IsParticipantOrReadOnly, IsOwnerOrReadOnlyList, IsUserPutOrOwnerDeleteOnly
from movieselector.serializers import UserSerializer, UserRegisterSerializer, UserInSelectionSerializer, UserInSelectionDetailSerializer, SelectionSerializer, VoteSerializer, MovieInSelectionSerializer
from rest_framework import generics, permissions
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


class UserInSelectionList(generics.ListCreateAPIView):
    serializer_class = UserInSelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyList,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return UserInSelection.objects.filter(selection__id=selection_id)

    def perform_create(self, serializer):
        selection_id = self.kwargs['selection_id']
        user = serializer.validated_data['user']
        users = UserInSelection.objects.filter(
            selection__id=selection_id,
            user=user);
        if len(users):
            raise ValidationError('User Already In Selection')
        selection = Selection.objects.get(id=selection_id)
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
        selection_id = self.kwargs['selection_id']
        selection = Selection.objects.get(id=selection_id)
        serializer.save(owner=self.request.user, selection=selection)


class MovieInSelectionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieInSelectionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return MovieInSelection.objects.filter(selection__id=selection_id).all()

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
        selection = Selection.objects.get(id=selection_id)
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
