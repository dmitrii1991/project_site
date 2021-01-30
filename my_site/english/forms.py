from django import forms

from .models import *

from django.forms import BaseFormSet
from django.forms import formset_factory

class WordForm(forms.ModelForm):
    class Meta:
        model = Word

        fields = ['word_rus', 'word_eng', 'category']
        widgets = {
            'word_rus': forms.TextInput(attrs={"class": "form-control"}),
            'word_eng': forms.TextInput(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-control"}),
        }

    def clean_word_rus(self):
        word_rus: str = self.cleaned_data['word_rus']
        word_rus = word_rus.capitalize()
        return word_rus

    def clean_word_eng(self):
        word_eng: str = self.cleaned_data['word_eng']
        word_eng = word_eng.capitalize()
        return word_eng