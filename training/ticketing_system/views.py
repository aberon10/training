# -*- coding: utf-8 -*-
import time
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from .forms import SignInForm
from .forms import LoginForm
from .forms import TicketCreateForm

from .models import User
from .models import Ticket


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
            user = User.objects.get(email=request.session['user'])
            tickets = Ticket.objects.filter(
                    Q(status='O'),
                    Q(author=user) | Q(assignee=user)
            ).distinct()
            return render(
                request,
                template_name=self.template_name,
                context={
                    'current_path': request.path.split('/')[1],
                    'tickets': tickets
                }
            )
        else:
            return HttpResponseRedirect('/login')


class TicketView(FormView):
    """ Ticket View. """

    form_class = TicketCreateForm
    template_name = 'ticketing_system/ticket_form.html'
    success_url = '/ticket'

    def get(self, request, *args, **kwargs):
        if not request.session.get('user'):
            return HttpResponseRedirect('/login')
        else:
            user = User.objects.get(email=request.session['user'])
            try:
                if kwargs['id_ticket']:
                    try:
                        ticket = Ticket.objects.filter(
                            Q(pk=int(kwargs['id_ticket'])),
                            Q(author=user) | Q(assignee=user)
                        )[0]
                    except Ticket.DoesNotExist:
                        return HttpResponseNotFound('<h1>Page not found</h1>')
                    else:
                        form = self.form_class(initial={
                            'title': ticket.title,
                            'body': ticket.body,
                            'author': ticket.author,
                            'created': ticket.created,
                            'status': ticket.status,
                        })
            except KeyError:
                form = self.form_class(initial={
                    'author': request.session['user'],
                    'created': time.strftime('%Y-%m-%d'),
                    'status': 'O',
                    'assignee': user.id
                })

            return render(
                request,
                template_name=self.template_name,
                context={'form': form}
            )

    def post(self, request, *args, **kwargs):
        if not request.session.get('user'):
            return HttpResponseRedirect('/login')
        else:
            error_message = ''
            ticket = Ticket()
            assignees_users = request.POST.getlist('assignee')
            form = TicketCreateForm({
                'title': request.POST.get('title'),
                'body': request.POST.get('body'),
                'status': request.POST.get('status'),
                'created': request.POST.get('created')
            })

            if form.is_valid():
                title = form.cleaned_data['title']
                body = form.cleaned_data['body']
                email = self.request.session['user']
                created = form.cleaned_data['created']
                status = form.cleaned_data['status']
                author = User.objects.get(email=email)

                try:
                    if kwargs['id_ticket']:
                        ticket = Ticket.objects.get(pk=int(kwargs['id_ticket']))
                        for item in ticket.assignee.all():
                            user = User.objects.get(pk=int(item.id))
                            ticket.assignee.remove(user)

                except KeyError:
                    pass

                try:
                    users = []
                    for user in assignees_users:
                        users.append(User.objects.get(pk=int(user)))
                except User.DoesNotExist:
                    error_message = 'Error creating ticket'
                else:
                    ticket.title = title
                    ticket.body = body
                    ticket.author = author
                    ticket.created = created
                    ticket.status = status
                    ticket.save()

                    if not users:
                        users.append(author)

                    ticket.assignee.set(users)
                    return HttpResponseRedirect('/dashboard')

            return render(
                request,
                template_name=self.template_name,
                context={
                    'form': TicketCreateForm(request.POST),
                    'error_message': error_message
                }
            )


class TicketDeleteView(TemplateView):

    def get(self, request, *args, **kwargs):
        if not request.session.get('user'):
            return HttpResponseRedirect('/login')
        else:
            try:
                if kwargs['id_ticket']:
                    user = User.objects.get(email=request.session['user'])
                    ticket = Ticket.objects.filter(
                                    Q(pk=int(kwargs['id_ticket'])),
                                    Q(author=user) | Q(assignee=user)
                            ).distinct()
                    ticket.delete()
            except KeyError:
                pass
            except Ticket.DoesNotExist:
                pass
        return HttpResponseRedirect('/dashboard')
