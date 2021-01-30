from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Word, Category, UserWord
from .forms import WordForm


class ListWords(ListView):
    model = Word
    context_object_name = 'words'
    paginate_by = 10

    def get_queryset(self):
        # print(dir(Word.objects.prefetch_related('users')[0].userword_set))
        # print(Word.objects.prefetch_related('users')[0].userword_set.values()[0]['error'])
        # print(Word.objects.prefetch_related('users')[0].userword_set.values_list())
        if self.request.user.is_authenticated:
            return Word.objects.prefetch_related('users').filter(users=self.request.user)
        return Word.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Английский'
        return context


class WordsByCategory(ListView):
    model = Word
    context_object_name = 'words'
    # allow_empty = False
    template_name = 'english/word_list.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Word.objects.prefetch_related('users').filter(users=self.request.user).filter(category_id=self.kwargs['category_id']).select_related('category')
        return Word.objects.filter(category_id=self.kwargs['category_id']).select_related('category')


class CreateWord(CreateView):
    form_class = WordForm
    template_name = 'english/add_word.html'
    success_url = reverse_lazy('english:english_title')
    raise_exception = True

    def form_valid(self, form):
        obj = form.save(commit=False)
        word_rus = obj.word_rus
        obj.save()
        word = Word.objects.get(word_rus=word_rus)
        user_word = UserWord()
        user_word.word = word
        user_word.user = self.request.user
        user_word.save()
        # return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)
