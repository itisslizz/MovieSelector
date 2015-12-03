from rest_framework import permissions


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

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Participants of a Selection to add movies.
    """

    def has_object_permission(self, request, view, obj):
        #
        #
        if request.method in permissions.SAFE_METHODS:
            return True

        print view
        if "MovieInSelection":
            selection = obj.selection
        elif "Votes":
            # not sure if this works
            selection = obj.movie_in_selection.selection

        # Write permissions are only allowed to participants of a Selection
        return request.user in obj.selection(users)
