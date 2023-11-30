from rest_framework import viewsets
from electronics_trade.models import Participant
from electronics_trade.permissions import IsActiveUser
from electronics_trade.serializers import ParticipantSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    Представления для участников (поставщиков)
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['contacts__country']  # Добавляем contacts__country для поиска по стране
    ordering_fields = ['level']  # Сортировка по уровням
    # Пример сортировки /electronics_trade/participants/?ordering=-level
    filterset_fields = ['contacts__country']  # Добавляем поле 'contacts__country' для фильтрации
    #  Пример фильтрации /electronics_trade/participants/?contacts__country=страна1
