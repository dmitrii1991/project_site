from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from .models import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}),
                               help_text='Имя пользователя должно быть не менее 3 символов')
    email = forms.EmailField(label='Почта пользователя', widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль 1', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Пароль 2', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'password1': forms.PasswordInput(attrs={"class": "form-control"}),
            'password2': forms.PasswordInput(attrs={"class": "form-control"}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='Email от кого', widget=forms.EmailInput(attrs={"class": "form-control"}))
    to = forms.EmailField(label='Email кому', widget=forms.EmailInput(attrs={"class": "form-control"}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control"}), label='Текст')


class CommentForm(forms.Form):
    name = forms.CharField(max_length=25, label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='Email от кого', widget=forms.EmailInput(attrs={"class": "form-control"}))
    body = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control"}), label='Текст')


class SearchForm(forms.Form):
    query = forms.CharField(label='Запрос', widget=forms.TextInput(attrs={"class": "form-control"}))


class PasswordChangeFormUser(PasswordChangeForm):
    old_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                   help_text='Введите текущий пароль')
    new_password1 = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                    help_text='Введите новый пароль')
    new_password2 = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                    help_text='Введите снова новый пароль')

