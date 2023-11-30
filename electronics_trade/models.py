from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Participant(models.Model):
    """Модель участника сети"""
    pass


class Contacts(models.Model):
    """Модель контактов участника"""
    pass


class Product(models.Model):
    """Модель продуктов участника"""
    pass
