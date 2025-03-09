from django.urls import path
from .views import HomePage, search_words

app_name = "Home"

urlpatterns = [
    path('', HomePage, name="Home"),
    path('search', search_words, name='search_words'),
]
