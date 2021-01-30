from django.urls import path
from django.views.decorators.cache import cache_page  # кэш 51 видео
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .views import *


app_name = 'general_logic'

urlpatterns = [
    # path('', PostListView.as_view(), name='home'),
    path('', post_list, name='home'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('search/', post_search, name='post_search'),

    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('password_change/', PasswordChangeViewTitle.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
