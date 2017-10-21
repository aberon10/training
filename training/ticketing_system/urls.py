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
]
