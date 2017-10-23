# -*- coding: utf-8 -*-
from django import forms
from .models import User
from .models import Ticket


CLASSES_INPUT_FIELD = {
    'class': 'form-control'
}


class SignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=CLASSES_INPUT_FIELD),
        max_length=150,
        label='Email'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs=CLASSES_INPUT_FIELD),
        min_length=8,
        max_length=60,
        help_text='Use at least 8 characters.',
        label='Password'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs=CLASSES_INPUT_FIELD),
        max_length=60,
        label='Confirm Password'
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs=CLASSES_INPUT_FIELD),
        max_length=150,
        label='Name')


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(attrs=CLASSES_INPUT_FIELD),
            'password': forms.PasswordInput(attrs=CLASSES_INPUT_FIELD),
        }


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'body', 'assignee', 'status', 'author', 'created']
        widgets = {
            'title': forms.TextInput(attrs=CLASSES_INPUT_FIELD),
            'body': forms.Textarea(attrs=CLASSES_INPUT_FIELD),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'value': 'O'
            }),
            'created': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }, format='%Y-%m-%d'),
            'assignee': forms.SelectMultiple(
                attrs={
                    'class': 'form-control  select-multiple'
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(TicketCreateForm, self).__init__(*args, **kwargs)
        self.fields['assignee'].required = False
        self.fields['author'].required = False
        self.fields['status'].required = False
        self.fields['created'].required = False
