from django.test import TestCase, RequestFactory
from electronics_trade.models import Participant, Contacts
from electronics_trade.admin import ParticipantAdmin, HasDebtFilter
from django.contrib import admin
from django.urls import reverse
from django.db.models import Q


class AdminTest(TestCase):
    """Тесты для админки"""
    def setUp(self):
        """Создаём нужные экземпляры классов для тестирования"""

        self.requests_factory = RequestFactory()  # Создаём объекты запросов
        self.participant_admin = ParticipantAdmin(Participant, admin.site)  # Создаём админ-интерфейс для Participant

        # Создаём участников сети

        self.factory = Participant.objects.create(
            name='Factory_admin_test',
            participant_type='Завод',
            level=0
        )
        self.retail = Participant.objects.create(
            name='Retail_admin_test',
            participant_type='Розничная сеть',
            supplier=self.factory,
            debt_to_supplier=100
        )
        self.individual = Participant.objects.create(
            name='Individual_admin_test',
            participant_type='Индивидуальный предприниматель',
            supplier=self.retail,
            debt_to_supplier=150
        )

        # Создаём контакты (города участников)

        self.factory_city = Contacts.objects.create(
            participant=self.factory,
            city='city1'
        )
        self.retail_city = Contacts.objects.create(
            participant=self.retail,
            city='city1'
        )
        self.individual_city = Contacts.objects.create(
            participant=self.individual,
            city='city2'
        )

    def test_get_supplier_link(self):
        """Проверка есть ли ссылка на поставщика на странице объекта"""
        link = self.participant_admin.get_supplier_link(self.retail)
        expected_url = reverse('admin:electronics_trade_participant_change', args=[self.factory.id])
        expected_html = '<a href="{}">{}</a>'.format(expected_url, self.factory.name)
        self.assertEqual(link, expected_html)

    def test_get_supplier_link_no_supplier(self):
        """Проверка есть ли ссылка на поставщика, когда поставщика нет"""
        link = self.participant_admin.get_supplier_link(self.factory)
        self.assertEqual(link, '-')

    def test_lookups(self):
        """Проверка есть ли окошко выбора для фильтрации задолженности"""
        request = self.requests_factory.get('/admin/electronics_trade/participant/')  # Создаём запрос
        # Далее мы вызываем HasDebtFilter и передаём запрос, пустой словарь так как не выбираем фильтрацию
        # Также передаём саму модель и её административный интерфейс
        filter_instance = HasDebtFilter(request, {}, Participant, self.participant_admin)
        lookups = filter_instance.lookups(request, self.participant_admin)

        expected_lookups = [
            ('yes', 'Есть задолженность'),
            ('no', 'Нет задолженности'),
        ]
        self.assertEqual(list(lookups), expected_lookups)

    def test_queryset_with_yes_value(self):
        """Проверка на выдачу списка участников с задолженностью"""
        request = self.requests_factory.get('/admin/electronics_trade/participant/', {'has_debt': 'yes'})
        filter_instance = HasDebtFilter(request, {'has_debt': 'yes'}, Participant, self.participant_admin)
        # Здесь нам необходим order_by для того, чтобы упорядочить оба набора объектов
        queryset = filter_instance.queryset(request, Participant.objects.all()).order_by('debt_to_supplier')

        expected_queryset = Participant.objects.filter(debt_to_supplier__gt=0).order_by('debt_to_supplier')
        self.assertQuerysetEqual(queryset, expected_queryset)

    def test_queryset_with_no_value(self):
        """Проверка на выдачу списка участников без задолженности"""
        request = self.requests_factory.get('/admin/electronics_trade/participant/', {'has_debt': 'no'})
        filter_instance = HasDebtFilter(request, {'has_debt': 'no'}, Participant, self.participant_admin)
        queryset = filter_instance.queryset(request, Participant.objects.all()).order_by('debt_to_supplier')

        expected_queryset = Participant.objects.filter(Q(debt_to_supplier=0) | Q(debt_to_supplier__isnull=True))\
            .order_by('debt_to_supplier')
        self.assertQuerysetEqual(queryset, expected_queryset)

    def test_clear_debt_to_supplier(self):
        """Проверка admin-action на удаление задолженности"""
        queryset = Participant.objects.filter(participant_type='Розничная сеть')
        self.participant_admin.clear_debt_to_supplier(None, queryset)
        self.retail.refresh_from_db()  # Получаем обновлённые данные из БД
        self.individual.refresh_from_db()
        self.assertEqual(self.retail.debt_to_supplier, 0)
        self.assertEqual(self.individual.debt_to_supplier, 150)
