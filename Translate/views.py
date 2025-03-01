from django.shortcuts import render
from googletrans import Translator

def translate_text(request):
    translated_text = None
    if request.method == "POST":
        text = request.POST.get("text")
        lang = request.POST.get("lang")
        
        if text:
            translator = Translator()
            translated_text = translator.translate(text, dest=lang).text

    return render(request, "Translate/translate.html", {"translated_text": translated_text , "text":text,})
