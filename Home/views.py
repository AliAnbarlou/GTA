from django.shortcuts import render
from Word.models import Words

def HomePage(request):
    return render(request, "Home/Home.html")

def search_words(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return render(request, 'Search/search_results.html', {'results': None, 'query': query, 'exact_match': None})

    exact_match = Words.objects.filter(word__iexact=query).first()
    results = Words.objects.filter(word__icontains=query)

    return render(request, 'Search/search_results.html', {
        'results': results,
        'query': query,
        'exact_match': exact_match
    })
