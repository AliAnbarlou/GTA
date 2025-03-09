from django.shortcuts import render
from Word.models import Words

def HomePage(request):
    return render(request, "Home/Home.html")

def search_words(request):
    query = request.GET.get('q', '').strip()

    # در صورتی که ورودی خالی باشد، تمپلیت نتایج با مقدار None نمایش داده شود
    if not query:
        return render(request, 'Search/search_results.html', {
            'results': None,
            'query': query,
            'exact_match': None
        })

    # بررسی وجود دقیق کلمه در دیتابیس
    exact_match = Words.objects.filter(word__exact=query).first()
    # جستجو برای کلماتی که شامل query هستند
    results = Words.objects.filter(word__icontains=query)

    # نمایش تمپلیت نتایج جستجو در هر دو حالت وجود یا عدم وجود کلمه در دیتابیس
    return render(request, 'Search/search_results.html', {
        'results': results,
        'query': query,
        'exact_match': exact_match
    })
