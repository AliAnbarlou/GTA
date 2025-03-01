from django.shortcuts import render , get_object_or_404
from Word.models import Words
# Create your views here.
def word_detail(request, word_slug):
    word = get_object_or_404(Words, slug=word_slug)
    return render(request, 'Word/word_detail.html', {'word': word})