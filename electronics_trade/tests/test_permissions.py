from django.test import TestCase
from users.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from electronics_trade.permissions import IsActiveUser


class IsActiveUserTest(TestCase):
    """Тесты на доступ к api представлениям активного и неактивного пользователя"""
    def setUp(self):
        """Создаём нужные экземпляры"""
        # Создаем активного пользователя
        self.active_user = User.objects.create_user(username='active_user', password='password')
        self.active_user.is_active = True
        self.active_user.save()

        # Создаем неактивного пользователя
        self.inactive_user = User.objects.create_user(username='inactive_user', password='password')
        self.inactive_user.is_active = False
        self.inactive_user.save()

    def test_has_permission_active_user(self):
        # Создаем запрос
        factory = APIRequestFactory()
        request = factory.get('/')

        # Присваиваем активного пользователя к запросу
        request.user = self.active_user

        # Создаем экземпляр класса IsActiveUser
        permission = IsActiveUser()

        # Проверяем, что активный пользователь имеет доступ
        self.assertTrue(permission.has_permission(request, APIView()))

    def test_has_permission_inactive_user(self):
        # Создаем запрос
        factory = APIRequestFactory()
        request = factory.get('/')

        # Присваиваем неактивного пользователя к запросу
        request.user = self.inactive_user

        # Создаем экземпляр класса IsActiveUser
        permission = IsActiveUser()

        # Проверяем, что неактивный пользователь не имеет доступа
        self.assertFalse(permission.has_permission(request, APIView()))
