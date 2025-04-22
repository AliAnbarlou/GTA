# Translate/views.py
from django.shortcuts import render
from googletrans import Translator

def translate_text(request):
    # set defaults so GET and POST share the same render call
    text = ""
    translated_text = ""
    lang = "en"   # default target

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        lang = request.POST.get("lang", "en")
        if text:
            translator = Translator()
            translated_text = translator.translate(text, dest=lang).text

    return render(request, "Translate/translate.html", {
        "text": text,
        "translated_text": translated_text,
        "lang": lang,
    })
