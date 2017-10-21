# -*- coding: utf-8 -*-
from django import forms
from .models import User


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
