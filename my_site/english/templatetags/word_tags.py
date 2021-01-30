from django import template
from django.db.models import Count


from ..models import Category, UserWord

register = template.Library()


@register.simple_tag
def show_categories():
    return Category.objects.all()

@register.simple_tag
def show_categories():
    return Category.objects.all()




