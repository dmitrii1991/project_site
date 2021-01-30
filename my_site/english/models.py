import os.path

from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User

from gtts import gTTS


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='имя категории', unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('english:category', kwargs={'category_id': self.pk})


class Word(models.Model):
    word_rus = models.CharField(max_length=255, verbose_name='RUS', primary_key=True)
    word_eng = models.CharField(max_length=255, verbose_name='ENG', unique=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    users = models.ManyToManyField(User, through='UserWord', through_fields=('word', 'user'))


    class Meta:
        ordering = ('word_eng',)
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'

    def __str__(self):
        return f'{self.word_rus} - {self.word_eng}'

    def get_music(self):
        path_misic = os.path.join(settings.MUSIC_ROOT, f'{self.word_eng}.mp3')
        if not os.path.exists(path_misic):
            tts = gTTS(self.word_eng)
            tts.save(path_misic)
        return os.path.join(settings.MUSIC_URL, f'{self.word_eng}.mp3')


class UserWord(models.Model):
    """Расширение ManyToManyField Word.users"""
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    error = models.IntegerField(default=0, verbose_name='ошибки')