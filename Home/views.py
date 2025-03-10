from django.shortcuts import render , get_object_or_404 , redirect
from django.urls import reverse
from Word.models import(
    Words ,
    Suggestion,
    Ask ,
    NewWords ,
    Response
)
import requests
from django.contrib import messages
DICTIONARY_CACHE = {}

def HomePage(request):
    return render(request, "Home/Home.html")

def GrandTheftAPI(word):
    if word in DICTIONARY_CACHE:
        return DICTIONARY_CACHE[word]
    
    url = f"https://engine2.vajehyab.com/search?q={word}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        result = {"خطا": "خطا در دریافت اطلاعات"}
        DICTIONARY_CACHE[word] = result
        return result
    
    dictionary_sections = data.get("wordbox", {}).get("sections", [])

    if not dictionary_sections:
        result = {"خطا": "تعریفی یافت نشد"}
        DICTIONARY_CACHE[word] = result
        return result

    section_mapping = {
        "meaning": "معنی",
        "alternative": "برابر پارسی",
        "synonym": "مترادف",
        "dictionary": "دیکشنری",
    }

    result = {section_mapping.get(item.get("section"), item.get("section")): item.get("description", "") for item in dictionary_sections}

    DICTIONARY_CACHE[word] = result
    return result

def add_suggestion(request, word_slug):
    if request.method == "POST":
        word = get_object_or_404(Words, slug=word_slug)
        text = request.POST.get('suggestion_text')
        user = request.user

        if text:
            # ایجاد پیشنهاد جدید
            Suggestion.objects.create(
                suggested_to=word,
                user=user,
                text=text,
                status='d'  # وضعیت پیشنهادی پیش‌فرض 'د'
            )
        messages.success(request, 'پیشنهاد شما ثبت شد. پس از تایید مدیر منتشر خواهد شد.')
        return redirect(f"{reverse('Home:search_words')}?q={word.word}")
  # بازگشت به صفحه جزئیات کلمه
def add_question(request, word_slug):
    if request.method == "POST":
        word = get_object_or_404(Words, slug=word_slug)
        text = request.POST.get('question_text')
        user = request.user

        if text:
            # ایجاد سوال جدید
            Ask.objects.create(
                ask_to=word,
                user=user,
                question=text
            )
        return redirect(f"{reverse('Home:search_words')}?q={word.word}")
def add_response(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Ask, id=question_id)
        response_text = request.POST.get('response_text')
        user = request.user

        if response_text:
            # ذخیره پاسخ جدید
            response = Response.objects.create(
                response_to=question,
                user=user,
                response=response_text
            )
            # ارسال پیام موفقیت
            messages.success(request, 'پاسخ شما با موفقیت ارسال شد.')
        else:
            # در صورتی که متنی وارد نشده باشد
            messages.error(request, 'لطفاً یک پاسخ وارد کنید.')

        return redirect(f"{reverse('Home:search_words')}?q={question.ask_to.word}")

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