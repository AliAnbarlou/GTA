from django.shortcuts import render
from Word.models import Words
#from articles.models import Article
def HomePage(request):
    return render(request,"Home/Home.html")
def search_words(request):
    query = request.GET.get('q', '')
    results = Words.objects.filter(word__icontains=query) if query else None
    return render(request, 'Search/search_results.html', {'results': results, 'query': query})