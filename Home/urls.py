from django.urls import path
from .views import *
urlpatterns = [
    path('', view=HomePage,name="Home"),
    path('search/', search_words, name='search_words'),
    path('Search/',view=search_word_list,name='search_word'),
]