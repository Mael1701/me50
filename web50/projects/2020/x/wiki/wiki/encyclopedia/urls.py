from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path('entry/<str:title>/', views.entry, name='entry'),
    path('random/', views.random_page, name='random_page'),
    path('new/', views.new_entry, name='new_entry'),
    path('entry/<str:title>/edit/', views.edit_entry, name='edit_entry'),
    path('search/', views.search, name='search'),
]
