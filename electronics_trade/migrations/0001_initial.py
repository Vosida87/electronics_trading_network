# Generated by Django 4.2.7 on 2023-11-30 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название участника')),
                ('participant_type', models.CharField(choices=[('Завод', 'Завод'), ('Розничная сеть', 'Розничная сеть'), ('Индивидуальный предприниматель', 'Индивидуальный предприниматель')], max_length=40, verbose_name='Тип участника')),
                ('debt_to_supplier', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Задолженность поставщику')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('level', models.IntegerField(editable=False, verbose_name='Уровень в иерархии')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='electronics_trade.participant', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('model', models.CharField(max_length=100, verbose_name='Модель')),
                ('release_date', models.DateField(verbose_name='Дата выхода продукта на рынок')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='electronics_trade.participant', verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Страна')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=100, null=True, verbose_name='Улица')),
                ('house_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер дома')),
                ('participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='electronics_trade.participant', verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
    ]
