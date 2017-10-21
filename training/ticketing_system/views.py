# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from .forms import SignInForm
from .forms import LoginForm

from .models import User


class LoginView(FormView):
    """ Login View. """

    form_class = LoginForm
    template_name = 'ticketing_system/login.html'
    success_url = '/dashboard'

    def get(self, request, *args, **kwargs):

        if request.session.get('user'):
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(
                request,
                template_name=self.template_name,
                context={'form': self.form_class}
            )

    def form_valid(self, form):
        context = {
            'form': form,
            'error_login': 'The user and/or password do not match'
        }

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if check_password(password, user.password):
                # create the new user session
                self.request.session['user'] = user.email
                self.request.session['name'] = user.name
                return HttpResponseRedirect(self.get_success_url())

        return render(
            self.request,
            template_name=self.template_name,
            context=context
        )


class LogoutView(RedirectView):
    """ Logout View. """

    url = '/login'

    def get(self, request, *args, **kwargs):
        try:
            # delete the user session
            del request.session['user']
            del request.session['name']
        except KeyError:
            pass
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(TemplateView):
    """ Register View. """

    template_name = 'ticketing_system/register.html'

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(
            request,
            template_name=self.template_name,
            context={'register_form': form}
        )

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        response = {
            'register_form': form,
            'message': '',
            'success': False
        }

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            name = form.cleaned_data['name']

            if password != confirm_password:
                response['register_form']['confirm_password'].error_messages =\
                    'Passwords do not match..'
            else:
                try:
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    user = User(
                        email=email,
                        name=name,
                        password=make_password(password)
                    )
                    user.save()

                    response['register_form'] = SignInForm()
                    response['success'] = True
                    response['message'] = 'You have successfully \
                    registered!'
                else:
                    response['register_form']['email'].error_messages = \
                        'User already exists'
        return render(
            request,
            template_name=self.template_name,
            context=response,
        )


class DashboardView(TemplateView):
    """ Dashboard View. """

    template_name = 'ticketing_system/dashboard.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('user'):
            return render(
                request,
                template_name=self.template_name
            )
        else:
            return HttpResponseRedirect('/login')
