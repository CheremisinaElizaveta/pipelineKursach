from django.contrib import admin
from users.models import User, Role, UserGroup
    

class UserAdmin(admin.ModelAdmin):
    # Добавляем поля для поиска
    search_fields = ['username', 'first_name', 'last_name', 'email']

    # Добавляем фильтрацию
    list_filter = ['is_active', 'is_staff', 'date_joined']

    # Настройка сортировки
    ordering = ['-date_joined']  # Сортировка по дате присоединения, по убыванию

    # Настройка отображаемых столбцов
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'date_joined']

    # Дополнительная настройка поля редактирования
    list_editable = ['is_active', 'is_staff']  # Сделать поля активными для редактирования


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(UserGroup)
