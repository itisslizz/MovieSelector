from movieselector.models import Selection, MovieInSelection, Vote, UserInSelection
from movieselector.permissions import IsOwnerOrReadOnly, IsParticipantOrReadOnly
from movieselector.serializers import UserSerializer, UserInSelectionSerializer, SelectionSerializer, VoteSerializer, MovieInSelectionSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return UserInSelection.objects.filter(selection__id=selection_id)

    def perform_create(self, serializer):
        selection_id = self.kwargs['selection_id']
        selection = Selection.objects.get(id=selection_id)
        serializer.save(selection=selection)

class UserInSelectionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInSelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return UserInSelection.objects.filter(selection__id=selection_id)


class MovieInSelectionList(generics.ListCreateAPIView):
    serializer_class = MovieInSelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return MovieInSelection.objects.filter(selection__id=selection_id)

    def perform_create(self, serializer):
        selection_id = self.kwargs['selection_id']
        selection = Selection.objects.get(id=selection_id)
        serializer.save(owner=self.request.user, selection=selection)


class MovieInSelectionDetail(generics.ListCreateAPIView):
    serializer_class = MovieInSelectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        return MovieInSelection.objects.filter(selection__id=selection_id)

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        voting_round = self.kwargs['voting_round']
        return UserInSelection.objects.filter(selection__id=selection_id).filter(voting_round=voting_round)

    def perform_create(self, serializer):
        voting_round = self.kwargs['voting_round']
        selection_id = self.kwargs['selection_id']
        selection = Selection.objects.get(id=selection_id)
        serializer.save(voter=self.request.user,
                        selection=selection,
                        voting_round = voting_round)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VoteSerializer

    def get_queryset(self):
        selection_id = self.kwargs['selection_id']
        voting_round = self.kwargs['voting_round']
        return UserInSelection.objects.filter(selection__id=selection_id).filter(voting_round=voting_round)
