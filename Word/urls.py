from django.urls import path
from .views import *
app_name = 'Word'  # این مهم است!

urlpatterns = [
    path('w/<str:word_slug>/', word_detail, name="word_detail"),  # مسیر جزئیات کلمه
    path('word/<slug:word_slug>/add-suggestion/', add_suggestion, name='add_suggestion'),
    path('word/<slug:word_slug>/add-question/', add_question, name='add_question'),
    path('response/<int:question_id>/', add_response, name='add_response'),
    path("api/<str:word>/", get_suggestion, name="vajehyab"),
]