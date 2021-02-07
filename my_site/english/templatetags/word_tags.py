from django import template
from django.db.models import Count
from django.core.cache import cache


from ..models import Category, UserWord

register = template.Library()


@register.simple_tag
def show_categories():
    category_obj = cache.get('all_subjects')
    if not category_obj:
        category_obj = Category.objects.all()
        cache.set('all_subjects', category_obj)
        return category_obj





