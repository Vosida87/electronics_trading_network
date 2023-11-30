from rest_framework import serializers

from electronics_trade.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['name', 'participant_type', 'supplier', 'debt_to_supplier', 'created_at', 'level']
        read_only_fields = ['debt_to_supplier']  # поле изменить через API запрос нельзя, только читать
