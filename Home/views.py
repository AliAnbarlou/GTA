from django.shortcuts import render , redirect
from Word.models import Words

#from articles.models import Article
def HomePage(request):
    return render(request,"Home/Home.html")
def search_words(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'Search/search_results.html', {'results': None, 'query': query})

    # بررسی وجود کلمه به‌صورت دقیق
    exact_match = Words.objects.filter(word__exact=query).first()
    if exact_match:
        return redirect('Word:word_detail', word_slug=exact_match.slug)  # فرض می‌کنیم صفحه جزئیات کلمه دارید

    # جستجوی کلماتی که شامل این کلمه هستند
    results = Words.objects.filter(word__icontains=query)
    
    return render(request, 'Search/search_results.html', {'results': results, 'query': query})
def search_word_list(request):
    query = request.GET.get('q', '').strip()
    results = Words.objects.filter(word__icontains=query)
    return render(request, 'Search/search_results.html', {'results': results, 'query': query})
