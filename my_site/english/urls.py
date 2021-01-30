from django.urls import path
from django.views.decorators.cache import cache_page  # кэш 51 видео

from .views import *

app_name = 'english'

urlpatterns = [
    path('', ListWords.as_view(), name='english_title'),
    path('category/<int:category_id>/', WordsByCategory.as_view(), name='category'),
    path('add_word/', CreateWord.as_view(), name='add_word'),
]
