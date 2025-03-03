from django.urls import path
from .views import *
app_name = 'Word'  # این مهم است!

urlpatterns = [
    path('w/<str:word_slug>/', word_detail, name="word_detail"),  # مسیر جزئیات کلمه
]