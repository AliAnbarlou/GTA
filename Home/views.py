from django.shortcuts import render , get_object_or_404
from Word.models import Words , Suggestion, Ask , NewWords
import requests
def HomePage(request):
    return render(request, "Home/Home.html")

def GrandTheftAPI(word):
    url = f"https://engine2.vajehyab.com/search?q={word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        dictionary_sections = data.get("wordbox", {}).get("sections", [])

        if (len(dictionary_sections) == 0):
            return {"error": "Failed to fetch data"}
        
        return {
            item["section"]: item["description"] for item in dictionary_sections
        }
    
    return {"error": "Failed to fetch data"}
def search_words(request):
    query = request.GET.get('q', '').strip()
    context = {
        'results': [],
        'exact_match': None,
        'query': query,
    }

    if not query:
        return render(request, 'Search/search_results.html', context)
    context['query'] = query
    exact_match = Words.objects.filter(word__iexact=query).first()
    results = Words.objects.filter(word__icontains=query)

    if exact_match:
        suggestions = Suggestion.objects.filter(suggested_to=exact_match, status='p')
        questions = Ask.objects.filter(ask_to=exact_match)
        context.update({'dict':GrandTheftAPI(query),})
        context.update({'word': exact_match, 'suggestions': suggestions, 'questions': questions})
    else:
        if not results:
            context.update({'dict':GrandTheftAPI(query),})
            NewWords.objects.get_or_create(word=query)
            return render(request, 'Search/no_results.html', context)
        else:
            context['results'] = results
            return render(request, 'Search/search_results.html', context)

    return render(request, 'Search/search_results.html', context)