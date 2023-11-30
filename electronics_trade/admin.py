from django.contrib import admin
from electronics_trade.models import Participant, Contacts, Product
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Q


class HasDebtFilter(admin.SimpleListFilter):
    """
    Фильтрация по задолженностям
    """
    title = 'Наличие задолженности'  # Заголовок фильтра
    parameter_name = 'has_debt'  # в URL

    def lookups(self, request, model_admin):
        """
        Список значений фильтра для выбора
        """
        return (
            ('yes', 'Есть задолженность'),
            ('no', 'Нет задолженности'),
        )

    def queryset(self, request, queryset):
        """
        Фильтрация на основе выбранного значения
        """
        if self.value() == 'yes':
            return queryset.filter(debt_to_supplier__gt=0)  # __gt - оператор фильтрации "больше чем"
        elif self.value() == 'no':
            return queryset.filter(Q(debt_to_supplier=0) | Q(debt_to_supplier__isnull=True))  # __isnull - если null


class ParticipantAdmin(admin.ModelAdmin):
    """
    Этот класс предоставляет функционал для настройки админ-панели
    """
    readonly_fields = ('get_supplier_link',)  # Только чтения
    list_filter = ('contacts__city', HasDebtFilter)  # Фильтрация записей
    actions = ['clear_debt_to_supplier']  # Действия в админке

    def get_supplier_link(self, obj):
        """
        Показывает ссылку поставщика объекта
        """
        if obj.supplier:  # Если есть поставщик
            url = reverse('admin:electronics_trade_participant_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '-'  # Если нет поставщика

    get_supplier_link.short_description = 'Ссылка на поставщика'  # Отображение в админке

    def clear_debt_to_supplier(self, request, queryset):
        """
        Admin action для удаления задолженности у объектов
        """
        queryset.update(debt_to_supplier=0)

    clear_debt_to_supplier.short_description = 'Очистить задолженность перед поставщиком'


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Contacts)
admin.site.register(Product)
