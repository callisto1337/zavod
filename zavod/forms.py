#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput, EmailField
from django.contrib.auth.forms import UserCreationForm
from zavod.models import Question
from zavod.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password")


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': TextInput(attrs={'id': 'inputText',
                                     'placeholder': 'Текст вопроса',
                                     'required': 1}),
        }
