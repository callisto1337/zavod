#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput
from zavod.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': TextInput(attrs={'id': 'inputText',
                                     'placeholder': 'Текст вопроса',
                                     'required': 1}),
        }
