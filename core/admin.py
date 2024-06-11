from django.contrib import admin
from . import models


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']  # список полей из таблицы для отоборажения в админке
    list_display_links = ['pk', 'title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'views', 'author', 'category', 'img_preview']
    list_display_links = ['pk', 'title']
    list_editable = ['author', 'category']
    readonly_fields = ['views']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment)
