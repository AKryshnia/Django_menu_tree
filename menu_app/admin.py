from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_name', 'parent', 'position')
    list_filter = ('menu_name',)
    search_fields = ('name',)
    list_editable = ('position',)
    autocomplete_fields = ['parent']
