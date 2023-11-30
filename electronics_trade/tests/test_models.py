from django.test import TestCase
from electronics_trade.models import Participant, Contacts, Product
from rest_framework.exceptions import ValidationError


class ParticipantTest(TestCase):
    """
    Тесты для модели участника и её методов
    """
    def setUp(self):
        """
        Создаём экземпляры завода, розничной сети и ИП
        """
        self.factory = Participant.objects.create(
            name='Factory',
            participant_type='Завод',
            level=0
        )
        self.retail = Participant.objects.create(
            name='Retail',
            participant_type='Розничная сеть',
            supplier=self.factory
        )
        self.individual = Participant.objects.create(
            name='Individual',
            participant_type='Индивидуальный предприниматель',
            supplier=self.retail
        )

    def test_str_representation(self):
        """
        Проверяет, что метод __str__ возвращает правильное представление участника
        """
        self.assertEqual(str(self.factory), 'Участник: Factory')
        self.assertEqual(str(self.retail), 'Участник: Retail')
        self.assertEqual(str(self.individual), 'Участник: Individual')

    def test_save_method(self):
        """
        Проверяет, что метод save правильно вычисляет и устанавливает уровень участника
        """
        self.assertEqual(self.factory.level, 0)
        self.assertEqual(self.retail.level, 1)
        self.assertEqual(self.individual.level, 2)

    def test_clean_method(self):
        """
        Проверяет, что метод clean работает правильно
        """
        invalid_participants = [
            Participant(name='Invalid_factory', participant_type='Завод', level=1),  # у завода level не может быть > 0
            Participant(name='Invalid_retail', participant_type='Розничная сеть', level=0),  # только у завода level = 0
            Participant(
                name='Invalid_factory2',
                participant_type='Завод',
                level=0,
                supplier=Participant(name='Invalid_factory'))  # У завода не может быть поставщика
        ]
        for participant in invalid_participants:
            with self.assertRaises(ValidationError):
                participant.clean()


class ContactsTest(TestCase):
    def setUp(self):
        self.factory = Participant.objects.create(
            name='Factory',
            participant_type='Завод',
            level=0
        )
        self.factory_city = Contacts.objects.create(
            participant=self.factory,
            city='city1'
        )

    def test_str_representation(self):
        """
        Проверяет, что метод __str__ возвращает правильное представление участника
        """
        self.assertEqual(str(self.factory_city), 'Контакты Участник: Factory')


class ProductsTest(TestCase):
    def setUp(self):
        self.factory = Participant.objects.create(
            name='Factory',
            participant_type='Завод',
            level=0
        )
        self.factory_product = Product.objects.create(
            owner=self.factory,
            title='product1',
            model='model1',
            release_date='2023-10-10'
        )

    def test_str_representation(self):
        """
        Проверяет, что метод __str__ возвращает правильное представление участника
        """
        self.assertEqual(str(self.factory_product), 'Продукт: product1, Участник: Factory')
