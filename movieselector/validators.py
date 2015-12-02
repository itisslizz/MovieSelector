from rest_framework import serializers

def is_next_or_current_round(value, id):
    selection = Selection.object(id)
    if (not selection.in_round + 1 == value) and (not slection.in_round == value) :
        raise serializers.ValidationError('Is not next or current round.')

def is_in_range(value):
    if value < 1:
        raise serializers.ValidationError('Is not in the allowed range.')
