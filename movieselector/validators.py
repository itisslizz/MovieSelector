from rest_framework import serializers
from movieselector.models import UserInSelection

def is_next_or_current_round(value, id):
    selection = Selection.object(id)
    if (not selection.in_round + 1 == value) and (not slection.in_round == value) :
        raise serializers.ValidationError('Is not next or current round.')

def is_in_range(value):
    if value < 1:
        raise serializers.ValidationError('Is not in the allowed range.')


class UniqueTogetherWithSelection(object):
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, values):
        if len(UserInSelection.objects.filter(user=value, selection=self.selection)):
            message = "User is already participating in selection"
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        self.selection = serializer_field.parent.selection
