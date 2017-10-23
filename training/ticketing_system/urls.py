# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'ticketing_system'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.LoginView.as_view(),
        name='login'
    ),
    url(
        regex=r'^login/$',
        view=views.LoginView.as_view(),
        name='login'
    ),
    url(
        regex=r'^register/$',
        view=views.RegisterView.as_view(),
        name='register'
    ),
    url(
        regex=r'^dashboard/$',
        view=views.DashboardView.as_view(),
        name='dashboard'
    ),
    url(
        regex=r'^logout/$',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        regex=r'^ticket/$',
        view=views.TicketView.as_view(),
        name='ticket'
    ),
    url(
        regex=r'^ticket/(?P<id_ticket>[0-9]+)/$',
        view=views.TicketView.as_view(),
        name='ticket'
    ),
    url(
        regex=r'^ticket/(?P<id_ticket>[0-9]+)/delete/$',
        view=views.TicketDeleteView.as_view(),
        name='ticket'
    ),
]
