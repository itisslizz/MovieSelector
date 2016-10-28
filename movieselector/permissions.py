from rest_framework import permissions
from movieselector.models import Selection

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsOwnerOrReadOnlyList(permissions.BasePermission):
    """
    Custom permission to only allow owner of selection to add users to it
    """

    def has_permission(self, request, view):
        #
        #
        if request.method in permissions.SAFE_METHODS:
            return True

        selection_id = view.kwargs['selection_id']
        # Write permissions are only allowed to participants of a Selection
        return request.user == Selection.objects.get(id=selection_id).owner

class IsUserPutOrOwnerDeleteOnly(permissions.BasePermission):
    """
    Custom permission to only allow responsible user to edit accepted value
    and owner of selection to delete users
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user

        # Write permissions are only allowed to the owner of the snippet.
        return obj.selection.owner == request.user

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Participants of a Selection to add movies.
    """

    def has_permission(self, request, view):
        #
        #
        if request.method in permissions.SAFE_METHODS:
            return True

        selection_id = view.kwargs['selection_id']
        return request.user in Selection.objects.get(id=selection_id).users.order_by('id')

class IsOwnerOfSelectionOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        selection_id = view.kwargs['selection_id']
        return request.user == Selection.objects.get(id=selection_id).owner
