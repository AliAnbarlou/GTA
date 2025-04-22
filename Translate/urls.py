from django.urls import path
from .views import translate_text

app_name = "Translate"

urlpatterns = [
    path("", translate_text, name="translate"),
]
