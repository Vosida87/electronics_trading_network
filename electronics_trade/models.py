from django.db import models
from rest_framework.exceptions import ValidationError

NULLABLE = {'null': True, 'blank': True}


class Participant(models.Model):
    """
    Модель участника сети
    Участниками могут быть заводы, розничные сети и ИП;
    Иерархия поставщиков по уровням начиная от 0, у завода всегда уровень равен 0.
    """
    PARTICIPANT_TYPES = (
        ('Завод', 'Завод'),
        ('Розничная сеть', 'Розничная сеть'),
        ('Индивидуальный предприниматель', 'Индивидуальный предприниматель'),
    )
    name = models.CharField(max_length=100, verbose_name='Название участника')
    participant_type = models.CharField(max_length=40, choices=PARTICIPANT_TYPES, verbose_name='Тип участника')
    supplier = models.ForeignKey('self', **NULLABLE, on_delete=models.SET_NULL, verbose_name='Поставщик')
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Задолженность поставщику',
                                           **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    level = models.IntegerField(verbose_name='Уровень в иерархии')

    class Meta:
        """
        Для отображения в админ-панели
        """
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f'Участник: {self.name}'

    def save(self, *args, **kwargs):
        """
        Автоматическое вычисление и установка уровня участника по следующему принципу:
        Если есть поставщик, то уровень участника на 1 выше чем у его поставщика
        """
        if self.supplier:
            self.level = self.supplier.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def clean(self):
        """
        Проверка на то, что у завода не может быть уровень отличный от 0
        Также только завод может иметь уровень 0
        """
        if self.participant_type == 'Завод' and self.level != 0:
            raise ValidationError("Завод может иметь только уровень 0")
        elif self.participant_type == 'Завод' and self.supplier:
            raise ValidationError("У завода не может быть поставщика")
        elif self.participant_type in ['Розничная сеть', 'Индивидуальный предприниматель'] and self.level == 0:
            raise ValidationError("Только завод может иметь уровень 0")
        super().clean()


class Contacts(models.Model):
    """
    Модель контактов участника
    """
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE, verbose_name='Участник')
    email = models.EmailField(**NULLABLE, verbose_name='Email')
    country = models.CharField(max_length=100, **NULLABLE, verbose_name='Страна')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='Город')
    street = models.CharField(max_length=100, **NULLABLE, verbose_name='Улица')
    house_number = models.CharField(max_length=20, **NULLABLE, verbose_name='Номер дома')

    class Meta:

        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'Контакты {self.participant}'


class Product(models.Model):
    """
    Модель продуктов участника
    """
    owner = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name='Владелец')
    title = models.CharField(max_length=100, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')

    class Meta:

        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.title}, {self.owner}'
