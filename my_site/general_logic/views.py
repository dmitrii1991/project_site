from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, View
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.db.models import Count
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.backends import ModelBackend as BaseBackend


from taggit.models import Tag

from .forms import *
from .models import *


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'general_logic/index.html'



class PostDetail(View):
    model = Post
    template_name = 'general_logic/detail.html'

    def get(self, request, year, month, day, post) -> HttpResponse:
        """Детальное отображение статьи

        :param request:
        :param year: год
        :param month: месяц
        :param day: день
        :param post: имя поста
        :return:
            HttpResponse
        """
        post = get_object_or_404(Post,
                                 slug=post,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
        comments = post.comments.filter(active=True)
        new_comment = None
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                #  Создаем комментарий, не сохраняя в БД для привязке к текущей статье
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
        else:
            comment_form = CommentForm()
        return render(
            request,
            'general_logic/detail.html',
            {
                'post': post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form': comment_form,
            })


def post_detail(request, year, month, day, post) -> HttpResponse:
    """Детальное отображение статьи

    :param request:
    :param year: год
    :param month: месяц
    :param day: день
    :param post: имя поста
    :return:
        HttpResponse
    """
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #  Создаем комментарий, не сохраняя в БД для привязке к текущей статье
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(
        request,
        'general_logic/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
        })


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'general_logic/index.html', {'page': page, 'posts': posts, 'tag': tag})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'general_logic/share.html', {'post': post, 'form': form})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        # Поиск по полям и по важности
        search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        search_query = SearchQuery(query)
        results = Post.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.3).order_by('-rank')
    return render(request, 'general_logic/search.html', {'form': form, 'query': query, 'results': results})


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)            # автоматическое создание профиля
            login(request, user, backend='general_logic.authentication.EmailAuthBackend')                         # для автоматической авторизации
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('general_logic:home')
        else:
            messages.error(request, 'ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'general_logic/register.html', {"form": form})


def user_logout(request):
    """Выход"""
    logout(request)
    return redirect('general_logic:login')


def user_login(request):
    """Регистрация"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='general_logic.authentication.EmailAuthBackend')
            return redirect('general_logic:home')
    else:
        form = UserLoginForm()
    return render(request, 'general_logic/register.html', {"form": form})


class PasswordChangeViewTitle(PasswordChangeView):
    form_class = PasswordChangeFormUser
    template_name = 'general_logic/password_change_form.html'
    success_url = reverse_lazy('general_logic:password_change_done')


class PasswordChangeDoneViewTitle(PasswordChangeDoneView):
    template_name = 'general_logic/password_change_done.html'


class PasswordResetViewTitle(PasswordResetView):
    email_template_name = 'general_logic/password_reset_ email.html'
    template_name = 'general_logic/password_reset_form.html'
    success_url = reverse_lazy('general_logic:password_reset_done')


@login_required
def edit_profile(request):
    # todo для отладки
    Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       files=request.FILES)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
    else:
        form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'general_logic/edit.html', {'user_form': form, 'profile_form': profile_form})
