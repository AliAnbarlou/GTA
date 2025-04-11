from django.urls import path
from .views import *

app_name = "Home"

urlpatterns = [
    path('', HomePage, name="Home"),
    path('search/', search_words, name='search_words'),
    path('word/<slug:word_slug>/add-suggestion/', add_suggestion, name='add_suggestion'),
    path('word/<slug:word_slug>/add-question/', add_question, name='add_question'),
    path('response/<int:question_id>/', add_response, name='add_response'),
    path('about-us/',aboutus ,name="about_us"),
    path('privacy/',privacy , name="privacy"),
    path('Contact-us/',Contactus,name='Contactus'),
    path('faq/',faq,name="faq"),
    path('mission/',mission,name="mission"),
]
