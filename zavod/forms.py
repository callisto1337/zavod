#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput, EmailField, Form, FileField, ClearableFileInput, CharField, Textarea, \
    NumberInput, IntegerField
from django.contrib.auth.forms import UserCreationForm
from zavod.models import Question, Subscription
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
        fields = ['text', 'type']
        widgets = {
            'text': TextInput(attrs={'id': 'inputText',
                                     'placeholder': 'Текст вопроса',
                                     'required': 1}),
            'type': NumberInput(attrs={'id': 'inputType',
                                       'placeholder': 'Тип вопроса',
                                       'required': False}),
        }


class CallbackForm(Form):
    name = CharField(max_length=200, required=True)
    email = EmailField(required=True)
    phone = CharField(max_length=50, required=True)
    comment = CharField(max_length=500, required=True)
    product = CharField(max_length=500, required=False)
    count = IntegerField(required=False)
    file_field = FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)


class CallMeForm(Form):
    name = CharField(max_length=200, required=True)
    phone = CharField(max_length=50, required=True)
    time_from = CharField(max_length=50, required=True)
    time_to = CharField(max_length=50, required=True)


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ("email",)

