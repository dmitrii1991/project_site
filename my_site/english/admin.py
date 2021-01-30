from django.contrib import admin

from .models import *


class UserWordInline(admin.TabularInline):
    model = UserWord
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


@admin.register(Word)
class WordsAdmin(admin.ModelAdmin):
    list_display = ('word_rus', 'word_eng', 'created', 'category')
    inlines = (UserWordInline,)


