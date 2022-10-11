from django.contrib import admin
from django.contrib.auth.models import Permission

from faq.models import Category, Faq


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'name']
    list_filter = ('name',)


@admin.register(Faq)
class AdminAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'question']
    list_filter = ('question',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'content_type',
        'codename',
    )
    list_filter = ('content_type',)
    search_fields = ['codename', 'name']

# EOF
